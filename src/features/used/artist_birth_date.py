"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""

from src.features.decorator_timing_feature import timing_feature
from src.features.array_feature import array_feature
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
from src.features.decorator_cached_feature import cached_feature
import musicbrainzngs
import pandas as pd
import datetime
import logging


@musicbrainz_feature
@cached_feature
@timing_feature
def artist_birth_date(artist_musicbrainz_id) -> 'date':
    """Extracts the date a solo artist is born, None otherwise.

    Arguments:
        artist_musicbrainz_id {str} -- 

    Returns:
        Pandas datetime object -- It is the conversion done using pandas.to_datetime of a string formatted as: YYYY-MM-DD. 
                                  This is the format in which much of the times this attribute is stored in musicbrainz.
                                  But, sometimes, happens that we know only the year. We are not interested in those cases
    """
    artist = musicbrainzngs.get_artist_by_id(artist_musicbrainz_id['value'])

    try:
        artist_type = artist['artist']['type']
    except KeyError:
        logging.getLogger('root.features').warning(
            f"Artist {artist_musicbrainz_id['value']} do not have a type, skipping")
        return None

    if artist['artist']['type'] == 'Person':
        try:
            birth_date = artist['artist']['life-span']['begin']
        except KeyError:
            logging.getLogger('root.features').warning(
                f"Artist {artist_musicbrainz_id['value']} do not have known a birth date")
            return None

        try:
            datetime.datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            logging.getLogger('root.features').warning(
                f"Incorrect artist_birth_date format for {artist_musicbrainz_id['value']}, should be YYYY-MM-DD, but got {birth_date}")
            return None

        try:
            birth_date_pandas = pd.to_datetime(birth_date)
        except pd.errors.OutOfBoundsDatetime:
            logging.getLogger('root.features').warning(
                f"Invalid artist_birth_date for {artist_musicbrainz_id['value']}: {birth_date}. Skipping")
            return None

        return {'value': birth_date_pandas}


if __name__ == "__main__":
    array_feature(artist_birth_date, mp=True)
