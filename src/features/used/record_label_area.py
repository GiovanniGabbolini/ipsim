"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""

from src.features.decorator_timing_feature import timing_feature
from src.features.array_feature import array_feature
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
import musicbrainzngs
import logging


@musicbrainz_feature
@timing_feature
def record_label_area(record_label_musicbrainz_id) -> 'area_musicbrainz_id':
    """Extracts the area the actual record label is based in

    Arguments:
        record_label_musicbrainz_id {str} --

    Returns:
        str -- The id of the area in musicbrainz
    """
    if record_label_musicbrainz_id is not None:
        label = musicbrainzngs.get_label_by_id(record_label_musicbrainz_id['value'])
        try:
            label_area_id = label['label']['area']['id']
            return {'value':label_area_id}
        except KeyError:
            logging.getLogger('root.features').warning(
                f"Record label {record_label_musicbrainz_id} has not area attribute")
            return None


if __name__ == "__main__":
    array_feature(record_label_area, mp=False)
