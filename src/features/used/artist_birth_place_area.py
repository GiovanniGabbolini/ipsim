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
def artist_birth_place_area(artist_musicbrainz_id) -> 'area_musicbrainz_id':
    """Extracts the area an artist was born, with its id in musicbrainz.

    Arguments:
        artist_musicbrainz_id {str} --

    Returns:
        str -- The id of the area in musicbrainz
    """
    if artist_musicbrainz_id is not None:
        artist = musicbrainzngs.get_artist_by_id(artist_musicbrainz_id['value'])
        try:
            birth_area_id = artist['artist']['begin-area']['id']
            return {'value':birth_area_id}
        except KeyError:
            logging.getLogger('root.features').warning(
                f"Artist {artist_musicbrainz_id} has not begin-area attribute")
            return None


if __name__ == "__main__":
    array_feature(artist_birth_place_area, mp=True)
