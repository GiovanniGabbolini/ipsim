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
def artist_type(artist_musicbrainz_id) -> 'artist_type':
    """States the type of the artist in musicbrainz.
       Artist can be Person, Group, Choir, Orchestra or Character (a finctional character).
       We discard Other in this method

    Arguments:
        artist_musicbrainz_id {str} -- 

    Returns:
        str -- Artist type
    """
    if artist_musicbrainz_id is not None:
        artist = musicbrainzngs.get_artist_by_id(artist_musicbrainz_id['value'])
        try:
            artist_type = artist['artist']['type']
            if artist_type != 'Other':
                return {'value': artist_type}
            else:
                return None
        except KeyError:
            logging.getLogger('root.features').warning(
                f"Artist {artist_musicbrainz_id} do not have a type, skipping")
            return None


if __name__ == "__main__":
    array_feature(artist_type, mp=False)
