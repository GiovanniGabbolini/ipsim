"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""


from src.features.decorator_timing_feature import timing_feature
from src.features.decorator_musicbrainz_feature import musicbrainz_feature
from src.features.decorator_cached_feature import cached_feature
from src.features.array_feature import array_feature
import musicbrainzngs
import logging


@musicbrainz_feature
@cached_feature
@timing_feature
def artist_wikidata_id(artist_musicbrainz_id) -> 'artist_wikidata_id':
    """Given the artist musicbrainz id, it returns the uri of its wikidata page.

    This allows us to retrieve the artist page in the 89% of the cases, and exploit
    the link that exists from artists pages from musicbrainz to wikidata.

    Arguments:
        artist_musicbrainz_id {str} --

    Returns:
        str -- wikidata artist uri
    """
    artist = musicbrainzngs.get_artist_by_id(
        artist_musicbrainz_id['value'], includes=['url-rels'])['artist']

    try:
        urls = artist['url-relation-list']
    except KeyError:
        logging.getLogger('root.features').warning(
            f"No relations to external pages specified for {artist_musicbrainz_id['value']}")
        return None

    url_wikidata = [u for u in urls if u['type'] ==
                    'wikidata' and u['direction'] == 'forward']
    if len(url_wikidata) > 0:
        return {'value': f"wd:{url_wikidata[0]['target'].split('/')[-1]}"}
    else:
        logging.getLogger('root.features').warning(
            f"No wikidata page specified for artist {artist_musicbrainz_id['value']}")
        return None


if __name__ == '__main__':
    array_feature(artist_wikidata_id, mp=True,)
