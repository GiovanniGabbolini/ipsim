"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""


from src.features.decorator_timing_feature import timing_feature
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
from src.features.decorator_cached_feature import cached_feature
import musicbrainzngs
import logging


@musicbrainz_feature
@cached_feature
@timing_feature
def artist_musicbrainz_id(artist_name) -> 'artist_musicbrainz_id':
    """Given an artist name, it returns the uri of its musicbrainz page.
    This uses the built-in entity linking functionalities in musicbrainz.

    Arguments:
        artist_name {str} - -

    Returns:
        uri - - Musicbrainz uri
    """
    result = musicbrainzngs.search_artists(artist=artist_name['value'], strict=True)
    if len(result['artist-list']) > 0:
        return {'value': result['artist-list'][0]['id']}
    else:
        logging.getLogger("root.features").warning(f"Could not find music brainz id for {artist_name['value']}")
