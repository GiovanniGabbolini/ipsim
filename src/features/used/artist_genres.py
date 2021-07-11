"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""

from src.features.decorator_timing_feature import timing_feature
from src.features.array_feature import array_feature
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
from src.features.decorator_cached_feature import cached_feature
import musicbrainzngs
import logging
from src.data.genres_musicbrainz import genres_musicbrainz


@musicbrainz_feature
@cached_feature
@timing_feature
def artist_genres(artist_musicbrainz_id) -> 'musical_genre_musicbrainz_id':
    """Extracts the musical genres interpreted by an artist.

    Arguments:
        artist_musicbrainz_id {str} -- 

    Returns:
        list -- List of musicbrainz genres ids. 
    """
    artist = musicbrainzngs.get_artist_by_id(
        artist_musicbrainz_id['value'], includes=['tags'])['artist']
    genres = []

    try:
        tags = artist['tag-list']
    except:
        logging.getLogger('root.features').warning(
            f"No tag list associated with artist {artist_musicbrainz_id['value']}")
        return None

    for tag in tags:
        try:
            musicbrainz_genre_id = genres_musicbrainz(tag['name'])
            genres.append(musicbrainz_genre_id)
        except KeyError:
            continue

    if len(genres) > 0:
        return [{'value': g} for g in genres]
    else:
        logging.getLogger('root.features').warning(
            f"No genres associated with artist {artist_musicbrainz_id['value']}")


if __name__ == "__main__":
    array_feature(artist_genres, mp=True)
