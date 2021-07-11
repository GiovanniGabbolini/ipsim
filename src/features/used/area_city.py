"""
Created on --

@author Giovanni Gabbolini
"""

import musicbrainzngs
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
from src.features.decorator_timing_feature import timing_feature
import logging


@musicbrainz_feature
@timing_feature
def area_city(area_musicbrainz_id) -> 'city_musicbrainz':
    """Given an area id in musicbrainz, returns the city associated with that area

    Returns:
        str -- 
    """
    city_id = _look_backward_recursive(area_musicbrainz_id['value'])
    if city_id is not None:
        return {'value': city_id}
    else:
        return None


def _look_backward_recursive(id_area):
    area = musicbrainzngs.get_area_by_id(
        id_area, includes=['area-rels'])['area']

    try:
        area_type = area['type']
    except KeyError:
        logging.getLogger('root.features').warning(
            f"Area {id_area} has no type, skipping")
        return None

    if area_type == 'City':
        return area['id']
    else:
        try:
            rels = area['area-relation-list']
        except KeyError:
            return None
        rels_backward = [r for r in rels if r['direction'] == 'backward']
        if len(rels_backward) > 0:
            return _look_backward_recursive(rels_backward[0]['target'])
        else:
            return None
