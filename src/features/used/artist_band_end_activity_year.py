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
import re


@musicbrainz_feature
@cached_feature
@timing_feature
def artist_band_end_activity_year(artist_musicbrainz_id) -> 'year':
    """For bands, extracts the year the band broke up, None otherwise.

    Returns:
        str -- Year, expressed as a string composed by four integers. Eg. 2001
    """
    if artist_musicbrainz_id is not None:
        artist = musicbrainzngs.get_artist_by_id(artist_musicbrainz_id['value'])

    try:
        artist_type = artist['artist']['type']
    except KeyError:
        logging.getLogger('root.features').warning(
            f"Artist {artist_musicbrainz_id['value']} do not have a type, skipping")
        return None

    if artist_type == 'Group':

        try:
            end_activity_year = artist['artist']['life-span']['end']
        except KeyError:
            logging.getLogger('root.features').warning(
                f"Band {artist_musicbrainz_id} do not have known end activity date")
            return None

        if re.match(r"^\d{4}$", end_activity_year):
            return {'value': end_activity_year}
        elif re.match(r"^\d{4}-\d{2}$", end_activity_year):
            return {'value': end_activity_year.split('-')[0]}
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", end_activity_year):
            return {'value': end_activity_year.split('-')[0]}
        else:
            logging.getLogger('root.features').warning(
                f"End activity year {end_activity_year} does not match pattern")


if __name__ == "__main__":
    array_feature(artist_band_end_activity_year, mp=False)
