"""
Created on --

@author Giovanni Gabbolini
"""

from src.data.genres_musicbrainz_to_wikidata import genres_musicbrainz_to_wikidata
from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def musical_genre_musicbrainz_to_wikidata(musical_genre_musicbrainz_id) -> 'musical_genre_wikidata':
    """Given the musical genre musicbrainz id, it returns the uri of its wikidata page.

    This exploits the link that exists of musical genres ids from musicbrainz to wikidata.

    The edge produced by this feature is not counted in interestingess's shortness heuristics.

    Arguments:
        musical_genre_musicbrainz_id {str} --

    Returns:
        str -- wikidata musical genre uri
    """
    genre_wikidata = genres_musicbrainz_to_wikidata(musical_genre_musicbrainz_id['value'])
    if genre_wikidata is not None:
        return {'value': genre_wikidata}
