from src.music_similarity.dataset import load_dataset
from src.music_similarity.algorithms.similarity import Random
from src.music_similarity.algorithms.segue_based_similarity import *
from src.music_similarity.algorithms.LDSD import LDSD
from pprint import pprint
from collections import OrderedDict
from src.music_similarity.benchmark.metrics import compute_accuracy_metrics, aggregate_metrics
import pandas as pd
from scipy.stats import wilcoxon
import logging
from src.utils.experiments import trunc


def similar_items(algorithms, dataset='mirex', cutoff=10, split='validation', save_similarity_matrix_if_not_exists=True):
    """Benchmark in the similar items task.
    It compute top-cutoff similar items to the items in similar_items_ground_truth.
    The candidate items are all those in the dataset.
    The top-cutoff similar items are compare against the the ground truth, similar_items_ground_truth.

    Args:
        algorithms (list of tuples): Algorithms for similarity, expressed as a list of tuples: (a, p)
                                        - a: algorithm class;
                                        - p: dictionary of parameter to be fed to constructor of algorithm class.
        dataset (str, optional): [description]. Defaults to 'mirex'.
        cutoff (int, optional): Handles lests of cutoffs. Defaults to 10. 
        use_saved_similarity_matrices (bool, optional)

    Returns:
        [type]: [description]
    """
    cutoff = [cutoff] if type(cutoff) == int else cutoff

    similar_items_ground_truth = load_dataset(dataset, f'similar_items_ground_truth_{split}')

    S = list(similar_items_ground_truth.keys())
    I = [item['id'] for item in load_dataset(dataset, 'items')]

    local_metrics = OrderedDict()
    global_metrics = {}

    for algorithm, params in algorithms:
        algorithm = algorithm(**params)
        matrix = algorithm.similarity_matrix(S, I, save_similarity_matrix_if_not_exists=save_similarity_matrix_if_not_exists)

        for row_index in range(matrix.shape[0]):
            row = matrix[row_index, :]
            top_n = [I[j] for j in sorted(range(len(I)), key=lambda j: -row[j])[:max(cutoff)]]
            ground_truth = similar_items_ground_truth[S[row_index]]

            if algorithm.name() in local_metrics:
                local_metrics[algorithm.name()].append(compute_accuracy_metrics(top_n, ground_truth, cutoff))
            else:
                local_metrics[algorithm.name()] = [compute_accuracy_metrics(top_n, ground_truth, cutoff)]

    return local_metrics
