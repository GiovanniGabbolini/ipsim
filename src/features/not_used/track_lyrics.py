'''
Created on Tue Jan 28 2020

@author Giovanni Gabbolini
'''


from src.features.decorator_cached_feature import cached_feature
from src.features.decorator_timing_feature import timing_feature
import lyricsgenius
from src.data import secret
from src.data import data
from src.features.read_feature_dataframe import read_feature_dataframe
from src.features.array_feature import array_feature
import logging
import time
import re
import requests

genius = lyricsgenius.Genius(secret.genius_key, verbose=False)


def exclude_lyrics(l):
    """Preprocess the lyrics, discarding those who do not have any of the tags reprted below
       Genius have lyrics formatted with the mentioned tags.
       If we do not filter out, random texts are catched if Genius can't find the song

       We seek for lyrics formatted like:
       "blabla[Chorus]bleble"

    Arguments:
        l {string} -- lyrics

    Returns:
        [str] -- Preprocessed lyrics
    """
    # We do not exclude if lyrics include among square brackets the reported tokens
    # If we match this format
    starting_condition = True
    recording = False
    count_to_close = 0

    s = ''
    for c in l:
        if c == '[' and starting_condition:
            starting_condition = False
            recording = True
            assert count_to_close == 0, "At this point, count to close shold be 0"
            count_to_close += 1
        elif c == '[' and recording:
            recording = False
            count_to_close += 1
        elif c == ']' and not recording:
            count_to_close = max(0, count_to_close-1)
            starting_condition = True if not count_to_close else False
        elif c == ']' and recording:
            assert count_to_close == 1, "At this point, count to close shold be 1"
            count_to_close -= 1
            starting_condition = True
            recording = False
            if re.search(r'(chorus|verse|intro|outro|hook|bridge)', s, re.I):
                return False
            s = ''
        s += c if recording and c != '[' else ''
    return True


@cached_feature
@timing_feature
def track_lyrics(track_name, artist_name) -> 'track_lyrics':
    """Retrieve the track lyrics by means of the genius APIs.

       TODO: Once the name of the tracks will be preprocessed and all the additional info
             contained in it will be harvested, in the cases in which now fails because of
             information contained in the title like Remix or Remastered, it should work better.
    """
    done = True
    while done:
        try:
            song = genius.search_song(track_name['value'], artist_name['value'])
            done = False
        except requests.exceptions.ReadTimeout as e:
            logging.getLogger('root.features').warning(
                f"A ReadTimeout exception happened while retrieving lyrics ... Rentryng ...")
            time.sleep(5)
        except TypeError as e:
            logging.getLogger('root.features').warning(
                f"An unexpected TypeError exception happened while retrieving lyrics ... Rentryng ...")
            time.sleep(5)
    if song:
        if not exclude_lyrics(song.lyrics):
            return {'value': song.lyrics}
        else:
            logging.getLogger('root.features').warning(
                f"Discarded lyrics {track_name['value']} by {artist_name['value']} because was not matching pattern")
            return None
    else:
        logging.getLogger('root.features').warning(
            f"I was not able to retrieve the lyrics for track {track_name['value']} by {artist_name['value']}")


def tracks_lyrics(**kwargs):
    track_df = read_feature_dataframe('track_name')
    track_album_artists_id = data.track_album_artists_id()
    artist_df = read_feature_dataframe('artist_name')
    df = track_df.merge(track_album_artists_id, how='left').merge(
        artist_df, how='left')
    argument_values = [df.track_name.values, df.artist_name.values]
    array_feature(track_lyrics, argument_values=argument_values, **kwargs)


if __name__ == "__main__":
    tracks_lyrics(mp=True)
