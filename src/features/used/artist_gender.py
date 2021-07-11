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


@musicbrainz_feature
@cached_feature
@timing_feature
def artist_gender(artist_musicbrainz_id) -> 'artist_gender':
    """States whether the gender of the artist.

    Arguments:
        artist_musicbrainz_id {str} -- 

    Returns:
        str -- 
    """
    if artist_musicbrainz_id is not None:
        artist = musicbrainzngs.get_artist_by_id(artist_musicbrainz_id['value'])
        try:
            artist_type = artist['artist']['gender']
        except KeyError:
            logging.getLogger('root.features').warning(
                f"Artist {artist_musicbrainz_id} has no gender, skipping")
            return None

        if artist['artist']['gender'] not in ['Male', 'Female']:
            logging.getLogger(
                f"Artist {artist_musicbrainz_id} has unknown gender {artist['artist']['gender']}, skipping")
            return None
        else:
            return {'value': artist['artist']['gender']}


if __name__ == "__main__":
    array_feature(artist_gender, mp=False)
