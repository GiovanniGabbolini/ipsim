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
def album_record_label(release_group_musicbrainz_id) -> 'record_label_musicbrainz_id':
    """Extracts the record label associated with an album.
       Taken the releases belonging to the release-group, the first valid record label is considered

    Returns:
        str -- if of the record label in musicbrainz
    """
    if release_group_musicbrainz_id is not None:
        releases = mz.browse_releases(release_group=release_group_musicbrainz_id['value'], includes=['labels'])

        for r in releases['release-list']:
            label_list = r['label-info-list']
            if len(label_list) > 0:
                for l in label_list:
                    try:
                        if l['label']['name'] != '[no label]':
                            return {'value': l['label']['id']}
                    except KeyError:
                        continue

            logging.getLogger('root.features').warning(
                f"Release {r['id']} has no associated record label")
            return None


if __name__ == "__main__":
    array_feature(album_record_label, mp=False)
