"""
Created on Wed Apr 16 2020

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
def artist_based_in_area(artist_musicbrainz_id) -> 'area_musicbrainz_id':
    """Extracts the area the actual artist is based in.

    Arguments:
        artist_musicbrainz_id {str} --

    Returns:
        str -- The id of the area in musicbrainz
    """
    if artist_musicbrainz_id is not None:
        artist = musicbrainzngs.get_artist_by_id(artist_musicbrainz_id['value'])
        try:
            birth_area_id = artist['artist']['area']['id']
            return {'value':birth_area_id}
        except KeyError:
            logging.getLogger('root.features').warning(
                f"Artist {artist_musicbrainz_id} has not area attribute")
            return None


if __name__ == "__main__":
    array_feature(artist_based_in_area, mp=True)
