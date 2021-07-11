"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""

from src.features.decorator_timing_feature import timing_feature
from src.features.array_feature import array_feature
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
from src.features.decorator_cached_feature import cached_feature
import musicbrainzngs as mz
import logging


@musicbrainz_feature
@cached_feature
@timing_feature
def artist_recorded_label(artist_musicbrainz_id) -> 'record_label_musicbrainz_id':
    """Harvest the list of record lables the artist has published records with,
    as musicbrainz record label ids.

    Arguments:
        artist_musicbrainz_id {str} -- 

    Returns:
        list -- Musicbrainz record lables ids.
    """
    releases = mz.browse_releases(artist=artist_musicbrainz_id['value'], includes=['labels'])
    labels = set()
    for r in releases['release-list']:
        label_list = r['label-info-list']
        for l in label_list:
            try:
                if l['label']['name'] != '[no label]':
                    labels.add(l['label']['id'])
            except KeyError:
                continue

    labels = list(labels)
    if len(labels) > 0:
        return [{'value': l} for l in labels]
    else:
        logging.getLogger('root.features').warning(
            f"I was not able to find any label for which artist {artist_musicbrainz_id['value']} has recorded")
        return None


if __name__ == "__main__":
    array_feature(artist_recorded_label, mp=True)
