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
from src.data import data
from src.features.read_feature_dataframe import read_feature_dataframe as rdf


@musicbrainz_feature
@cached_feature
@timing_feature
def release_group_id(album_name, artist_name) -> 'release_group_musicbrainz_id':
    """Retrieves the release-group in musicbrainz associated to an album made by an artist.

    Arguments:
        album_name {str} -- 
        artist_name {str} -- 

    Returns:
        str -- release group id in musicbrainz.
    """
    releases = musicbrainzngs.search_release_groups(
        album_name['value'], strict=True, artist=artist_name['value'])['release-group-list']
    filtered_releases = []
    for r in releases:
        try:
            if r['primary-type'] in ['Album', 'Single', 'EP']:
                filtered_releases.append(r)
        except KeyError:
            pass

    if len(filtered_releases) > 0:
        r = filtered_releases[0]['id']
        return {'value': r}
    else:
        logging.getLogger('root.features').warning(
            f"No release-group associate with album {album_name} by {artist_name}")
        return None


def _release_groups_id(**kwargs):
    artist_name = rdf('artist_name')
    album_name = rdf('album_name')

    # Correction to track_album_artist_id dataframe:
    # based on how it is created, an album can have more than one author
    # Infact, it is track-indexed in principle: for every track, it tells author and album
    # if in an album there are two different authors (e.g., compilation), then we will
    # have more author associated to that album. In develop, we force just one manually like this
    track_album_artists_id = data.track_album_artists_id()
    track_album_artists_id = track_album_artists_id[[
        'alid', 'arid']].drop_duplicates().groupby('alid').head(1)

    df = album_name.merge(track_album_artists_id, how='left', on='alid').merge(
        artist_name, how='left', on='arid')

    assert len(df) == len(album_name)

    argument_values = [df.album_name.values, df.artist_name.values]

    array_feature(release_group_musicbrainz_id, argument_values=argument_values, **kwargs)


if __name__ == "__main__":
    release_groups_id(mp=True)
