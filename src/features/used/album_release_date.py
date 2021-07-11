"""
Created on Wed Apr 22 2020

@author Giovanni Gabbolini
"""

from src.features.decorator_timing_feature import timing_feature
from src.features.array_feature import array_feature
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
from src.features.decorator_cached_feature import cached_feature
import musicbrainzngs
import logging
import datetime
import pandas as pd


@musicbrainz_feature
@cached_feature
@timing_feature
def album_release_date(release_group_musicbrainz_id) -> 'date':
    """Retrieves the date an album was released. It relies on the first-release-date attribute
    of a release group in musicbrainz

    Arguments:
        release_group_musicbrainz_id {str} --

    Returns:
        Pandas datetime object -- It is the conversion done using pandas.to_datetime of a string formatted as: YYYY-MM-DD. 
    """
    if release_group_musicbrainz_id is not None:
        release_group = musicbrainzngs.get_release_group_by_id(release_group_musicbrainz_id['value'])['release-group']

        try:
            date = release_group['first-release-date']
        except KeyError:
            logging.getLogger('root.features').warning(
                f"Release-group {release_group_musicbrainz_id['value']} has not first-release-date attribute")
            return None

        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            logging.getLogger('root.features').warning(
                f"Incorrect first release date format for {release_group_musicbrainz_id['value']}, should be YYYY-MM-DD, but got {date}")
            return None

        try:
            date_pandas = pd.to_datetime(date)
        except pd.errors.OutOfBoundsDatetime:
            logging.getLogger('root.features').warning(
                f"Invalid artist_date for {release_group_musicbrainz_id['value']}: {date}. Skipping")
            return None

        return {'value': date_pandas}


if __name__ == "__main__":
    array_feature(album_release_date, mp=False)
