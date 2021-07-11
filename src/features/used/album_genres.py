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
from src.data.genres_musicbrainz import genres_musicbrainz


@musicbrainz_feature
@cached_feature
@timing_feature
def album_genres(release_group_musicbrainz_id) -> 'musical_genre_musicbrainz_id':
    """Retrieves the musical genre associated to a musical album.
    In particular, it considers the genres associated with a release-group.

    Arguments:
        release_group_musicbrainz_id {str} --

    Returns:
        list -- id of the music genres in musicbrainz
    """
    if release_group_musicbrainz_id is not None:
        release_group = musicbrainzngs.get_release_group_by_id(release_group_musicbrainz_id['value'], includes=['tags'])['release-group']
        try:
            tags = release_group['tag-list']
        except KeyError:
            logging.getLogger('root.features').warning(
                f"Release-group {release_group_musicbrainz_id} has not tags")
            return None

        genres = []
        for tag in tags:
            try:
                musicbrainz_genre_id = genres_musicbrainz(tag['name'])
                genres.append(musicbrainz_genre_id)
            except KeyError:
                continue

        if len(genres) > 0:
            return [{'value': g} for g in genres]
        else:
            logging.getLogger('root.features').warning(
                f"No genres associated with release-group {release_group_musicbrainz_id}")
            return None


if __name__ == "__main__":
    array_feature(album_genres, mp=True)
