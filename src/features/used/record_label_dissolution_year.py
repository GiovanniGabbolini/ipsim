"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""

from src.features.decorator_timing_feature import timing_feature
from src.features.array_feature import array_feature
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
import musicbrainzngs
import logging
import re


@musicbrainz_feature
@timing_feature
def record_label_dissolution_year(record_label_musicbrainz_id) -> 'year':
    """Extracts the year a record label stopped to exist.

    Returns:
        str --
    """
    if record_label_musicbrainz_id is not None:
        label = musicbrainzngs.get_label_by_id(record_label_musicbrainz_id['value'])

        try:
            start_activity_year = label['label']['life-span']['end']
        except KeyError:
            logging.getLogger('root.features').warning(
                f"Label {record_label_musicbrainz_id} does not have known dissolution date")
            return None

        if re.match(r"^\d{4}$", start_activity_year):
            return {'value':start_activity_year}
        elif re.match(r"^\d{4}-\d{2}$", start_activity_year):
            return {'value':start_activity_year.split('-')[0]}
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", start_activity_year):
            return {'value':start_activity_year.split('-')[0]}
        else:
            logging.getLogger('root.features').warning(
                f"Record label dissolution year {start_activity_year} does not match pattern")


if __name__ == "__main__":
    array_feature(record_label_dissolution_year, mp=False)
