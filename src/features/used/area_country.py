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
def area_country(area_musicbrainz_id) -> 'country_musicbrainz':
    """Given an area id in musicbrainz, returns the country associated with that area

    Returns:
        str -- 
    """
    country_id = _look_backward_recursive(area_musicbrainz_id['value'])
    if country_id is not None:
        return {'value': country_id}
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

    if area_type == 'Country':
        return area['id']
    elif area_type == 'Subdivision':
        # The 50 states of USA are considered subdivisions. I consider them to be countries.
        if area['name'] in ['Alabama',
                            'Alaska',
                            'Arizona',
                            'Arkansas',
                            'California',
                            'Colorado',
                            'Connecticut',
                            'Delaware',
                            'Florida',
                            'Georgia',
                            'Hawaii',
                            'Idaho',
                            'Illinois',
                            'Indiana',
                            'Iowa',
                            'Kansas',
                            'Kentucky',
                            'Louisiana',
                            'Maine',
                            'Maryland',
                            'Massachusetts',
                            'Michigan',
                            'Minnesota',
                            'Mississippi',
                            'Missouri',
                            'Montana',
                            'Nebraska',
                            'Nevada',
                            'New Hampshire',
                            'New Jersey',
                            'New Mexico',
                            'New York',
                            'North Carolina',
                            'North Dakota',
                            'Ohio',
                            'Oklahoma',
                            'Oregon',
                            'Pennsylvania',
                            'Rhode Island',
                            'South Carolina',
                            'South Dakota',
                            'Tennessee',
                            'Texas',
                            'Utah',
                            'Vermont',
                            'Virginia',
                            'Washington',
                            'West Virginia',
                            'Wisconsin',
                            'Wyoming']:
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
