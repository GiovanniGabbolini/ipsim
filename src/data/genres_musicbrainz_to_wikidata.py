import numpy as np
from src.sparql.query_sparql_wikidata import query_sparql
import sys
from tqdm import tqdm
import logging
from src.data.data import preprocessed_dataset_path


def build_genres_musicbrainz_to_wikidata_dict():
    """Construct the dictionary for the associations between musicbrainz id and wikidata id

    Raises:
        FileNotFoundError: When the musicrainz genres dictionary is missing. It records which are the possible musicbrainz ids,
        and so it will constitute the keys of the dictionary that we are building here
    """
    sys.setrecursionlimit(10000)
    try:
        d = np.load(f'{preprocessed_dataset_path}/musicbrainz_genres_dictionary.npy',
                    allow_pickle=True).item()
    except FileNotFoundError:
        raise FileNotFoundError(
            "Musicbrainz genres dictionary is missing. Create using function build_genres_dictionary in genres_musicbrainz.py")

    musicbrainz_ids = list(d.values())
    musicbrainz_to_wikidata = {}
    for musicbrainz_id in tqdm(musicbrainz_ids):
        query = 'select ?i where{?i wdt:P8052 "' + musicbrainz_id + '"}'
        results = query_sparql(query)
        if len(results) == 1:
            wikidata_id = f"wd:{results[0]['i']['value'].split('/')[-1]}"
            musicbrainz_to_wikidata[musicbrainz_id] = wikidata_id
        else:
            logging.getLogger('root.data.build_genres_musicbrainz_to_wikidata_dict').warning(
                f"Found {len(results)} correspondences for genre {musicbrainz_id} in wikidata. Skipping")

    np.save(f'{preprocessed_dataset_path}/genres_musicbrainz_to_wikidata', musicbrainz_to_wikidata)


def genres_musicbrainz_to_wikidata(key):
    """Given a id of a genre in musicbrainz, returns the corresponding wikidata identity.
    We ensure that for every musicbrainz genre a wikidata page exists

    Arguments:
        key {str} -- musicbrainz id

    Returns:
        str -- wikidata page, in the shape wd:something
    """
    try:
        d = np.load(f'{preprocessed_dataset_path}/genres_musicbrainz_to_wikidata.npy',
                    allow_pickle=True).item()
    except FileNotFoundError:
        raise FileNotFoundError(
            "Genres musicbrainz to wikidata dictionary is missing. Create using function build_genres_musicbrainz_to_wikidata_dict in genres_musicbrainz_to_wikidata.py")

    try:
        return d[key]
    except KeyError:
        return None


if __name__ == "__main__":
    build_genres_musicbrainz_to_wikidata_dict()
