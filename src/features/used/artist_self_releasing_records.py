"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""

from src.features.decorator_timing_feature import timing_feature
from src.features.array_feature import array_feature
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
from src.features.decorator_cached_feature import cached_feature
import musicbrainzngs as mz


@musicbrainz_feature
@cached_feature
@timing_feature
def artist_self_releasing_records(artist_musicbrainz_id) -> 'artist_self_releasing_records':
    """Tell if the artist have self released records (i.e. without label) or not.

    Arguments:
        artist_musicbrainz_id {str} -- 

    Returns:
        bool --
    """
    releases = mz.browse_releases(artist=artist_musicbrainz_id['value'], includes=['labels'])
    for r in releases['release-list']:
        label_list = r['label-info-list']
        for l in label_list:
            try:
                if l['label']['name'] == '[no label]':
                    return {'value': True}
            except KeyError:
                continue


if __name__ == "__main__":
    array_feature(artist_self_releasing_records, mp=True)
