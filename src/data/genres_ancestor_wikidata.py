'''
Created on Thu Jan 30 2020

@author Giovanni Gabbolini
'''

from src.sparql.query_sparql_wikidata import query_sparql
import sys
import numpy as np
import logging
from tqdm import tqdm
from src.data.data import preprocessed_dataset_path


def build_genres_ancestor_wikidata_dict():
    """Construct the wikidata genre ancestors dictionary

    Raises:
        FileNotFoundError: It relies on the file genres_musicbrainz_to_wikidata which states which genres we can encounter,
                           that is, the genres in wikidata that correspond to the possible genres in musicbrainz
    """
    sys.setrecursionlimit(10000)
    try:
        d = np.load(f'{preprocessed_dataset_path}/genres_musicbrainz_to_wikidata.npy',
                    allow_pickle=True).item()
    except FileNotFoundError:
        raise FileNotFoundError(
            "Genres musicbrainz to wikidata dictionary is missing. Create using function build_genres_musicbrainz_to_wikidata_dict in genres_musicbrainz_to_wikidata.py")

    wikidata_ids = list(d.values())
    d = {}
    for wikidata_id in tqdm(wikidata_ids):
        query = 'select ?i where{' + wikidata_id + ' wdt:P279 ?i}'
        results = query_sparql(query)
        if len(results) > 0:
            ancestors = [
                f"wd:{r['i']['value'].split('/')[-1]}" for r in results]
            d[wikidata_id] = ancestors
        else:
            logging.getLogger('root.data.genres_ancestor_wikidata').warning(
                f"No ancestors found for the music genre {wikidata_id}")

    np.save(f'{preprocessed_dataset_path}/genres_ancestor_wikidata', d)


def genres_ancestor_wikidata(key):
    """Given a genre id in wikidata, returns its ancestors, if any

    Raises:
        FileNotFoundError: If the genres ancestor dictionary is missing, tell to create it
        KeyError: If the genre does not have ancestors

    Returns:
        list -- List of genres ancestors pages
    """
    try:
        d = np.load(f'{preprocessed_dataset_path}/genres_ancestor_wikidata.npy',
                    allow_pickle=True).item()
    except FileNotFoundError:
        raise FileNotFoundError(
            "Genres ancestor wikidata dictionary is missing. Create using function build_genres_ancestor_wikidata_dict in genres_ancestor_wikidata.py")

    try:
        return d[key]
    except KeyError:
        raise KeyError(
            f"{key} does not have musical ancestors")


if __name__ == "__main__":
    build_genres_ancestor_wikidata_dict()
