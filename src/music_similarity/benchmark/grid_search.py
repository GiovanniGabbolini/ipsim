from src.music_similarity.algorithms.LDSD import LDSD
from src.music_similarity.benchmark.recommendation import recommendation, retrieve_similarity_matrix
from src.music_similarity.benchmark.metrics import aggregate_metrics
from src.music_similarity.benchmark.similar_items import similar_items
from src.music_similarity.algorithms.segue_based_similarity import SegueBasedSimilarity, count_segues
from src.music_similarity.algorithms.similarity import Random
from itertools import product
import numpy as np
from tqdm import tqdm
import json
from src.data.data import preprocessed_dataset_path


def write_down(task, algorithm_name, params, values, dataset_name):
    path = f"{preprocessed_dataset_path}/similarity/{dataset_name}/grid_search_{task}_{algorithm_name}.json"
    try:
        with open(path) as f:
            l = json.load(f)
    except FileNotFoundError:
        l = []
    l.append({**params, **values})
    with open(path, 'w') as f:
        json.dump(l, f, ensure_ascii=False, indent=4)


def get_search_space(task, algorithm_name, dataset_name):
    """Returns the search space of an algorithm.
    It is a list of dictionary, and every dictionary is a point in the space.

    Args:
        algorithm_name (str)
    """

    def interestingness_weights_combinations():
        """Interestingness weights should sum to 1, so they cannot vary independently from each others.
        """
        ticks = np.array([.0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1])
        combinations = list(product(ticks, ticks, ticks))
        return_value = []
        for c in combinations:
            if sum(c) == 1:
                return_value.append(c)
        return return_value

    if task == 'recommendation':

        if dataset_name == 'lastfmrecommender':
            top_ks = [1, 3, 5, 7, 10, 20, 30, 40, None]
        elif dataset_name == 'facebookrecommender':
            top_ks = [1, 3, 5, 7, 10, 15, None]
        elif dataset_name == 'lastfmrecommendercelma':
            top_ks = [1, 3, 5, 7, 10, 25, 50, 75, 100, 175, 250, 375, 500, 750, 1000, None]

        recommender_params = [{'top_k': top_k} for top_k in top_ks]

        if algorithm_name == 'ipsim_strategy':

            n_hops = [(e+5)*2+1 for e in [2, np.inf]]
            interestingness_weights = interestingness_weights_combinations()
            search_space = list(product(n_hops, interestingness_weights))
            similarity_params = [{'n_hop': n_hop, 'rar_w': interestingness_weights[0], 'unpop_w': interestingness_weights[1],
                                  'shortness_w': interestingness_weights[2]} for n_hop, interestingness_weights in search_space]
        elif algorithm_name == 'LDSD':
            similarity_params = [{}]
        elif algorithm_name == 'count_segues':
            similarity_params = [{}]
        elif algorithm_name == 'random':
            similarity_params = [{}]

        return_value = (similarity_params, recommender_params)

    elif task == 'similar_items':

        if algorithm_name == 'ipsim_strategy':
            n_hops = [(e+5)*2+1 for e in [2, np.inf]]
            interestingness_weights = interestingness_weights_combinations()

            search_space = list(product(n_hops, interestingness_weights))
            return_value = [{'n_hop': n_hop, 'rar_w': interestingness_weights[0], 'unpop_w': interestingness_weights[1],
                             'shortness_w': interestingness_weights[2]} for n_hop, interestingness_weights in search_space]

    return return_value


def get_algorithm(algorithm_name, dataset_name, similarity_params):

    if algorithm_name == 'ipsim_strategy':

        def strategy(segues_interestingness_raw):
            elements = [e for e in segues_interestingness_raw if e[3] <= similarity_params['n_hop'] and e[0] != -np.inf and e[1] != -np.inf]
            segues_interestingness_refined = [i[0]*similarity_params['rar_w'] + i[1] *
                                              similarity_params['unpop_w'] + i[2] * similarity_params['shortness_w'] for i in elements]
            score = sum(segues_interestingness_refined)
            return score

        return_value = SegueBasedSimilarity(**{'dataset': dataset_name, 'aggregation_strategy': strategy})

    elif algorithm_name == 'LDSD':
        return_value = LDSD(**{'dataset': dataset_name})

    elif algorithm_name == 'count_segues':
        return_value = SegueBasedSimilarity(**{'dataset': dataset_name, 'aggregation_strategy': count_segues})

    elif algorithm_name == 'random':
        return_value = Random(dataset_name)

    return return_value


def checked_yet(task, algorithm_name, dataset_name, similarity_params):
    path = f"{preprocessed_dataset_path}/similarity/{dataset_name}/grid_search_{task}_{algorithm_name}.json"
    return_value = False
    try:

        with open(path) as f:
            l = json.load(f)

        for d in l:
            found = True

            for k in similarity_params.keys():
                try:
                    found = found and d[k] == similarity_params[k]
                except KeyError:
                    found = False

            if found:
                return_value = True
                break

    except FileNotFoundError:
        pass

    return return_value


def grid_search_recommendation(algorithm_name, dataset_name):
    cutoffs = [1, 3, 5, 10, 20, 50, 100]
    metric = ['accuracy', 'surprise']
    task = 'recommendation'
    sp, rp = get_search_space(task, algorithm_name, dataset_name)

    for similarity_params in tqdm(sp):

        if not checked_yet(task, algorithm_name, dataset_name, similarity_params):

            algorithm = get_algorithm(algorithm_name, dataset_name, similarity_params)
            similarity_matrix = retrieve_similarity_matrix(algorithm, dataset_name, save_similarity_matrix_if_not_exists=False)
            for recommender_params in rp:
                local_metrics = recommendation(similarity_matrix, dataset_name, cutoff=cutoffs,
                                               top_k=recommender_params['top_k'], metrics=metric, split='validation')
                results = aggregate_metrics(local_metrics)
                write_down(task, algorithm_name, {**similarity_params, **recommender_params}, results, dataset_name)


def grid_search_similar_items(algorithm_name, dataset_name):
    cutoffs = [1, 3, 5, 10, 20, 50, 100]
    task = 'similar_items'
    search_space = get_search_space(task, algorithm_name, dataset_name)

    for params in tqdm(search_space):
        algorithm = get_algorithm(algorithm_name, dataset_name, params)
        results = similar_items(algorithm, dataset_name, cutoff=cutoffs, split='validation', save_similarity_matrix_if_not_exists=False)
        write_down(task, algorithm_name, params, results[algorithm_name], dataset_name)


if __name__ == '__main__':
    grid_search_recommendation('LDSD', 'lastfmrecommender')
