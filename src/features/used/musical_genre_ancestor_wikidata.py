"""
Created on --

@author Giovanni Gabbolini
"""

from src.data.genres_ancestor_wikidata import genres_ancestor_wikidata
import logging


def musical_genre_ancestor_wikidata(musical_genre_wikidata) -> 'musical_genre_wikidata':
    """Extracts the ancestors of a musical genre, on the WikiData hierarchy

    Returns:
        [str]: musical genre wikidata ids.
    """
    try:
        ancestors = genres_ancestor_wikidata(musical_genre_wikidata['value'])
        return [{'value': a} for a in ancestors]
    except KeyError:
        logging.getLogger('root.features').warning(
            f"Genre {musical_genre_wikidata['value']} does not have known ancestors")
