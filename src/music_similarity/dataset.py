from src.knowledge_graph.applicable_actions import InformativeActionSupplier
from src.knowledge_graph.construct_graph import construct_graph
from src.knowledge_graph.merge_graphs import merge_graphs
from src.data.data import preprocessed_dataset_path, raw_dataset_path
from src.knowledge_graph.applicable_actions import CustomReturnValueMockedActionsSupplier
from src.utils.musicbrainz_setup import musicbrainzngs_setup
from src.utils.utils_ngx_graph import artist_id, artist_name
from src.sparql.query_sparql_dbpedia import query_sparql
from tqdm import tqdm
import json
import os
import re
import networkx as nx
import random
import numpy as np
import musicbrainzngs


def save_dataset(dataset):
    """Save a dataset for similarity.

    It needs a file items.json in the folder: {preprocessed_dataset_path}/similarity/{dataset}/items.json.
    items.json is in array json format, and every entry should have this format:
    {
        'id': unique identifier of the item
        'seed': dictionary to be fed into the construct_graph method
    }

    It creates a joint KG featuring all the items, and saves it.
    The ids of the source nodes in the KG are are dataset dependent.
    This method works cross-dataset.
    """

    with open(f"{preprocessed_dataset_path}/similarity/{dataset}/items.json") as f:
        items = json.load(f)

    graphs = []

    for item in tqdm(items):

        # using just factual nodes for similarity, leading to informative segues

        if dataset == 'mirex' or dataset == 'lastfmapi' or dataset == 'facebookrecommender':
            # custom initilizer, seed has also artist_musicbrainz_id, to be handled separately
            g = construct_graph(item['seed'], supplier=InformativeActionSupplier(), initializer=custom_construct_graph_initializer)
        else:
            g = construct_graph(item['seed'], supplier=InformativeActionSupplier())

        graphs.append(g)

    # in items node in joint graph, store also items sub-graph g, useful for similarity computation
    if dataset == 'mirex' or dataset == 'lastfmapi' or dataset == 'facebookrecommender':
        joint_graph = merge_graphs([lambda: graphs], strategy_fields_source_node=lambda g: {'graph': g}, strategy_graph_id=artist_id)
    else:
        joint_graph = merge_graphs([lambda: graphs], strategy_fields_source_node=lambda g: {'graph': g}, strategy_graph_id=artist_name)

    # save graph
    nx.write_gpickle(joint_graph, f"{preprocessed_dataset_path}/similarity/{dataset}/graph")


def load_dataset(dataset='mirex', what='graph'):

    base_path = f"{preprocessed_dataset_path}/similarity/{dataset}/"

    if what == 'graph':
        path = base_path+what
        object_requested = nx.read_gpickle(f"{preprocessed_dataset_path}/similarity/{dataset}/graph")

    elif what == 'urm':
        path = base_path+f"{what}.npy"
        object_requested = np.load(path)

    else:
        path = base_path+f"{what}.json"
        with open(path) as f:
            object_requested = json.load(f)

    return object_requested

# Facebook recommender.


def prepare_facebook_recommender_dataset():

    def map_dbpedia_uri_to_musicbrainz_uri(dbpedia_uri):
        query = "select ?x { <" + dbpedia_uri + "> owl:sameAs ?x . }"

        try:
            results = [e['x']['value'] for e in query_sparql(query)]
        except Exception:
            results = []
            print(f"Exception occourred while querying for {dbpedia_uri}, skipping")

        regexp = re.compile(r'http://musicbrainz\.org/artist/[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}')
        mb_uri = [r.split('/')[-1] for r in results if regexp.match(r)]
        if len(mb_uri) == 1:
            return mb_uri[0]
        else:
            return None

    raw_folder_path = f"{raw_dataset_path}/lod-challenge-2015"
    preprocessed_folder_path = f"{preprocessed_dataset_path}/similarity/facebookrecommender"
    os.makedirs(preprocessed_folder_path, exist_ok=True)
    random.seed(42)

    musicbrainzngs_setup()

    # The items in this dataset are of the following types (filter 1):
    # - 'music_album';
    # - 'music_artist';
    # - 'music_band';
    # - 'music_composition';
    # - 'music_genre'.
    # We are interested only on music_artists and music_bands, or artists for short.
    # We further filter out artists such that:
    # - Have interactions with at least 5 users (filter 2);
    # - The dbpedia id can be mapped to a valid musicbrainz id (filter 3);

    print("Filter 1")
    dbpedia_uris = []
    artists = []
    with open(f"{raw_folder_path}/items_music.dat", encoding="ISO-8859-1") as f:
        for line in f.read().split('\n')[1:-1]:
            # for line in f.read().split('\n')[1:10]:
            artist_id = line.split('\t')[0]
            entity_type = line.split('\t')[1]
            dbpedia_uri = line.split('\t')[2]

            if entity_type == 'music_band' or entity_type == 'music_artist':
                artists.append(artist_id)
                dbpedia_uris.append(dbpedia_uri)

    # Make sure that artists ids and dbpedia uris are unique.
    assert len(artists) == len(set(artists))
    assert len(dbpedia_uris) == len(set(dbpedia_uris))

    print("Filter 2")
    d_i_u = {}
    with open(f"{raw_folder_path}/training_likes_music.dat", encoding="ISO-8859-1") as f:
        for line in f.read().split('\n')[1:-1]:
            u_id = line.split('\t')[0]
            i_id = line.split('\t')[1]

            try:
                # Notice: training_likes_music does not contain duplicates -> an element appended was not there before.
                d_i_u[i_id].append(u_id)
            except KeyError:
                d_i_u[i_id] = [u_id]

    mask = [True]*len(artists)
    for idx, artist in enumerate(artists):
        if artist not in d_i_u or len(d_i_u[artist]) < 5:
            mask[idx] = False
    artists = [artists[i] for i, e in enumerate(mask) if e]
    dbpedia_uris = [dbpedia_uris[i] for i, e in enumerate(mask) if e]

    print("Filter 3")
    mb_uris = []
    for dbpedia_uri in tqdm(dbpedia_uris):
        mb_uri = map_dbpedia_uri_to_musicbrainz_uri(dbpedia_uri)
        mb_uris.append(mb_uri)
    artists = [artists[i] for i, e in enumerate(mb_uris) if e is not None]
    mb_uris = [mb_uris[i] for i, e in enumerate(mb_uris) if e is not None]

    # Make sure that mb uris are unique
    assert len(mb_uris) == len(set(mb_uris))

    items = []
    for a, u in tqdm(zip(artists, mb_uris)):
        try:
            artist_name = musicbrainzngs.get_artist_by_id(u)['artist']['name']
        except Exception:
            # Musicbrainz ids might not be valid, in such cases we skip them.
            continue

        d = {
            'id': u,
            'original_id': a,
            'seed': {
                'artist_musicbrainz_id': u,
                'artist_name': artist_name,
            }
        }
        items.append(d)

    with open(f"{preprocessed_folder_path}/items.json", 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

    items = load_dataset('facebookrecommender', 'items')

    artists = [d['original_id'] for d in items]
    artists_set = set(artists)
    artists_idx = {v: k for k, v in enumerate(artists)}
    mb_uris = [d['id'] for d in items]

    # Notice: every user has at least 15 interaction with items, before preprocessing.
    # After item preprocessing, 46 users will have interaction with less then 5 artists, but we keep them.
    print("Creating users")
    users = set()
    with open(f"{raw_folder_path}/training_likes_music.dat", encoding="ISO-8859-1") as f:
        for line in tqdm(f.read().split('\n')[1:-1]):
            u_id = line.split('\t')[0]
            i_id = line.split('\t')[1]
            if i_id in artists_set:
                users.add(u_id)
    users = list(users)

    # Build URM: users on the rows; artists on the columns; and likes as values i.e. either 0 (not like) or 1 (like).
    print("Creating URM")
    urm = np.zeros((len(users), len(artists)), dtype=np.uint8)
    users_set = set(users)
    users_idx = {v: k for k, v in enumerate(users)}

    with open(f"{raw_folder_path}/training_likes_music.dat") as f:
        for line in tqdm(f.read().split('\n')[1:-1]):
            u_id = line.split('\t')[0]
            i_id = line.split('\t')[1]

            if u_id in users_set and i_id in artists_set:
                idx_row = users_idx[u_id]
                idx_col = artists_idx[i_id]
                assert urm[idx_row][idx_col] == 0
                urm[idx_row][idx_col] = 1

    print("Creating held-out")
    held_out_validation = {}
    held_out_test = {}
    # create hold-out with 40% of user profile, 20 for validation and 20 for test
    for idx_row in range(urm.shape[0]):
        row = urm[idx_row, :]

        indices_interactions = list(np.nonzero(row)[0])

        # sample 40 percent of the interactions.
        k = len(indices_interactions)*40//100
        sample = random.sample(indices_interactions, k)

        sample_validation = sample[:len(sample)//2]
        sample_test = sample[len(sample)//2:]
        held_out_validation[idx_row] = [mb_uris[i] for i in sample_validation]
        held_out_test[idx_row] = [mb_uris[i] for i in sample_test]

        urm[idx_row, sample] = 0

    print("Saving them all")
    with open(f"{preprocessed_folder_path}/held_out_validation.json", 'w', encoding='utf-8') as f:
        json.dump(held_out_validation, f, ensure_ascii=False, indent=4)

    with open(f"{preprocessed_folder_path}/held_out_test.json", 'w', encoding='utf-8') as f:
        json.dump(held_out_test, f, ensure_ascii=False, indent=4)

    np.save(f"{preprocessed_folder_path}/urm", urm)


# LastFM-recommender Grouplens.


def listening_count_to_rating(urm):
    """Transform listening count in user profiles to ratings from 1 to 5.
    Based on O. Celma, Music Recommendations and Discovery in the Long Tail, pp 80-81.

    Args:
        urm (np array): user-item matrix, for element is the listening count of an user with an item.
    """
    for i in range(urm.shape[0]):
        u = [(j, c) for j, c in zip(np.nonzero(urm[i, :])[0], urm[i, np.nonzero(urm[i, :])[0]])]
        u = sorted(u, key=lambda e: e[1])
        l = sum([c for _, c in u])
        agg = 0
        for j, c in u:
            agg += c

            if agg <= 0.2*l:
                urm[i, j] = 1
            elif agg > 0.2*l and agg <= 0.4*l:
                urm[i, j] = 2
            elif agg > 0.4*l and agg <= 0.6*l:
                urm[i, j] = 3
            elif agg > 0.6*l and agg <= 0.8*l:
                urm[i, j] = 4
            elif agg > 0.8*l:
                urm[i, j] = 5

    return urm


def prepare_lastfm_recommender_dataset():
    random.seed(42)
    interactions_type = 'numerical'

    raw_folder_path = f"{raw_dataset_path}/hetrec2011-lastfm-2k"
    preprocessed_folder_path = f"{preprocessed_dataset_path}/similarity/lastfmrecommender"
    os.makedirs(preprocessed_folder_path, exist_ok=True)

    musicbrainzngs_setup()

    # Compute users list: users ids that have interacted with at least five different artists.
    map_user_id_to_interaction_count = {}
    with open(f"{raw_folder_path}/user_artists.dat") as f:
        for line in f.read().split('\n')[1:-1]:
            user_id = line.split('\t')[0]

            try:
                map_user_id_to_interaction_count[user_id] += 1
            except KeyError:
                map_user_id_to_interaction_count[user_id] = 1
    users = list({k: v for k, v in map_user_id_to_interaction_count.items() if v >= 5}.keys())

    # Ensures that there are not duplicates
    assert len(users) == len(set(users))

    # Compute artists list: artist names that had at least five interactions,
    # made by users that have interacted with at least five different artists.
    artists = []
    map_artist_id_to_artist_name = {}
    with open(f"{raw_folder_path}/artists.dat") as f:
        for artist_idx, line in enumerate(f.read().split('\n')[1:-1]):

            artist_id = line.split('\t')[0]
            artist_name = line.split('\t')[1]

            artists.append(artist_name)
            map_artist_id_to_artist_name[artist_id] = artist_name

    # Ensures that there are not duplicates
    assert len(artists) == len(set(artists))

    map_artist_name_to_interaction_count = {}
    with open(f"{raw_folder_path}/user_artists.dat") as f:
        for line in f.read().split('\n')[1:-1]:
            user_id = line.split('\t')[0]
            if user_id in users:
                artist_id = line.split('\t')[1]
                artist_name = map_artist_id_to_artist_name[artist_id]

                try:
                    map_artist_name_to_interaction_count[artist_name] += 1
                except KeyError:
                    map_artist_name_to_interaction_count[artist_name] = 1

    artists = list({k: v for k, v in map_artist_name_to_interaction_count.items() if v >= 5}.keys())

    # Build URM: users on the rows; artists on the columns; and number of interactions as values.
    # Notice, number of interaction is not listening count, but thresholded to either 0 or 1.
    urm = np.zeros((len(users), len(artists)), dtype=np.uint32)

    with open(f"{raw_folder_path}/user_artists.dat") as f:
        for line in f.read().split('\n')[1:-1]:
            user_id = line.split('\t')[0]
            artist_name = map_artist_id_to_artist_name[line.split('\t')[1]]
            listening_count = int(line.split('\t')[2])
            if user_id in users and artist_name in artists:

                idx_row = users.index(user_id)
                idx_col = artists.index(artist_name)

                assert urm[idx_row][idx_col] == 0
                urm[idx_row][idx_col] = listening_count

    # Test that urm has been filled correctly. If so, every artists should have at least five interactions.
    for idx_col in range(urm.shape[1]):
        assert np.count_nonzero(urm[:, idx_col]) >= 5

    items = []
    for artist_name in artists:
        d = {
            'id': artist_name,
            'seed': {
                'artist_name': artist_name,
            }
        }
        items.append(d)

    # transform listening counts in ratings
    urm = listening_count_to_rating(urm)

    I = [item['id'] for item in items]
    held_out_validation = {}
    held_out_test = {}

    # create hold-out with 20% of user profile
    for idx_row in range(urm.shape[0]):
        row = urm[idx_row, :]

        indices_interactions = list(np.nonzero(row)[0])

        # sample 40 percent of the interactions: 5->1, 7->1, 10->2, ...
        k = len(indices_interactions)*40//100
        sample = random.sample(indices_interactions, k)

        sample_validation = sample[:len(sample)//2]
        sample_test = sample[len(sample)//2:]
        held_out_validation[idx_row] = [I[i] for i in sample_validation if row[i] >= 4]
        held_out_test[idx_row] = [I[i] for i in sample_test if row[i] >= 4]

        urm[idx_row, sample] = 0

    with open(f"{preprocessed_folder_path}/items.json", 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

    with open(f"{preprocessed_folder_path}/held_out_validation.json", 'w', encoding='utf-8') as f:
        json.dump(held_out_validation, f, ensure_ascii=False, indent=4)

    with open(f"{preprocessed_folder_path}/held_out_test.json", 'w', encoding='utf-8') as f:
        json.dump(held_out_test, f, ensure_ascii=False, indent=4)

    np.save(f"{preprocessed_folder_path}/urm", urm)


# LastFM and Mirex top-n similar artists task.


def prepare_mirex_lastfmapi_dataset(which='mirex'):
    """Utility method for converting dataset from mirex and latfm to our format.

    It creates items.json, a and ground truth for similar items (similar_items_ground_truth.json)

    The datasets are from Oramas et al. "A Semantic-based Approach for Artist Similarity",
    downloaded from https://zenodo.org/record/1291810#.X85HTC9Q1E9
    """
    assert which in ['lastfmapi', 'mirex']

    raw_folder_path = f"{raw_dataset_path}/dataset_similarity_oramas_et_al"
    preprocessed_folder_path = f"{preprocessed_dataset_path}/similarity/{which}"
    os.makedirs(preprocessed_folder_path, exist_ok=True)
    musicbrainzngs_setup()

    # create items.json:
    # an entry for every artist present in mirex_gold.txt, including also those in the top-n most similar list.

    artists = []
    with open(f"{raw_folder_path}/{which}_gold.txt") as f:
        for line in f.read().split('\n')[:-1]:

            # artists with a ground truth of less than 10 items should be excluded, according to the paper
            if len(line.split('\t')[1].split(' ')) >= 10:
                artists += [line.split('\t')[0]]+line.split('\t')[1].split(' ')

    artists = list(set(artists))
    items = []
    for a in tqdm(artists):
        artist_name = musicbrainzngs.get_artist_by_id(a)['artist']['name']
        d = {
            'id': a,
            'seed': {
                'artist_musicbrainz_id': a,
                'artist_name': artist_name,
            }
        }
        items.append(d)

    with open(f"{preprocessed_folder_path}/items.json", 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

    # create similar_items_ground_truth.json

    ground_truth_validation = {}
    ground_truth_test = {}
    with open(f"{raw_folder_path}/{which}_gold.txt") as f:
        for line in f.read().split('\n')[:-1]:

            # artists with a ground truth of less than 10 items should be excluded, according to the paper
            if len(line.split('\t')[1].split(' ')) >= 10:
                held_out = line.split('\t')[1].split(' ')

                sample = random.sample(held_out, len(held_out))
                sample_validation = sample[:len(sample)//2]
                sample_test = sample[len(sample)//2:]
                ground_truth_validation[line.split('\t')[0]] = sample_validation
                ground_truth_test[line.split('\t')[0]] = sample_test

    with open(f"{preprocessed_folder_path}/similar_items_ground_truth_validation.json", 'w', encoding='utf-8') as f:
        json.dump(ground_truth_validation, f, ensure_ascii=False, indent=4)

    with open(f"{preprocessed_folder_path}/similar_items_ground_truth_test.json", 'w', encoding='utf-8') as f:
        json.dump(ground_truth_test, f, ensure_ascii=False, indent=4)


def custom_construct_graph_initializer(seed):
    """Initiliazer to be used as argument of construct_graph, 
       in case artist_musicbrainz_id is provided in seed, e.g. in Mirex.

       The graph is initialized with two nodes,
       artist_name and artist_musicbrainz_id, one son of the other,
       with values as defined in seed.

    Args:
        seed (dict)
    """
    g = construct_graph(seed, supplier=CustomReturnValueMockedActionsSupplier(
        {'artist_musicbrainz_id': seed.pop('artist_musicbrainz_id')}))
    return g


if __name__ == "__main__":
    prepare_mirex_lastfmapi_dataset('lastfmapi')
    save_dataset('lastfmapi')
