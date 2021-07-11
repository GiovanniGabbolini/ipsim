from src.music_similarity.dataset import load_dataset
from src.music_similarity.algorithms.similarity import Random
from src.music_similarity.algorithms.segue_based_similarity import *
from src.music_similarity.algorithms.LDSD import LDSD
from src.music_similarity.benchmark.metrics import *
from src.data.data import preprocessed_dataset_path
from collections import OrderedDict
import pandas as pd
import logging
import pprint


def arg_max_rows(matrix, cutoff):
    """Return the cutoffs indices associated to the highest values on the rows of matrix.

    Args:
        matrix (numpy array)
        cutoff (int)
    """
    # Pre-filtering, use argpartition to get indices of top-cutoff values on the rows of matrix, but shuffled.
    # Notice that argpartition runs in linear time!
    top_n_indices_unsorted = np.argpartition(-matrix, cutoff)[:, :cutoff]
    top_n_values_unsorted = np.take_along_axis(matrix, top_n_indices_unsorted, 1)

    # Sort filtered matrix ..
    temp = np.argsort(-top_n_values_unsorted)
    # .. and map back the temporary indices
    top_n_indices_sorted = np.take_along_axis(top_n_indices_unsorted, temp, 1)
    return top_n_indices_sorted


def compute_predictions_with_top_k(urm, similarity_matrix, top_k):
    """Score for a user (u) and item (i) pair is computed by summing
    the similarity scores of the top-k similar items in the user profile with i.

    Args:
        urm (np array)
        similarity_matrix (np array)
        top_k (int)
    """
    predictions = [None]*urm.shape[0]
    for row_idx in range(urm.shape[0]):
        non_zero_indices_urm_row = np.nonzero(urm[row_idx, :])[0]

        masked_similarity_matrix = similarity_matrix[:, non_zero_indices_urm_row]
        top_k_indices = np.argsort(-masked_similarity_matrix)[:, :top_k]

        mask = np.ma.array(masked_similarity_matrix, mask=True)
        np.put_along_axis(mask.mask, top_k_indices, False, axis=1)
        masked_similarity_matrix[mask.mask] = 0

        urm_similarity_weighted = urm[row_idx, non_zero_indices_urm_row]*masked_similarity_matrix
        predictions[row_idx] = np.sum(urm_similarity_weighted, axis=1)
    predictions = np.vstack(predictions)
    return predictions


def compute_predictions_without_top_k(urm, similarity_matrix):
    """Score for a user (u) and item (i) pair is computed by summing
    the similarity scores of the items in the user profile with i.

    Args:
        urm (np array)
        similarity_matrix (np array)
    """
    predictions = np.dot(urm, similarity_matrix.T)
    return predictions


def compute_predictions(urm, similarity_matrix, top_k=None):
    """Compute predictions. It accepts top-k, and will take care to call the appropriate method.

    Args:
        urm (np array)
        similarity_matrix (np array)
        top_k (int)
    """
    if top_k is None:
        predictions = compute_predictions_without_top_k(urm, similarity_matrix)
    else:
        predictions = compute_predictions_with_top_k(urm, similarity_matrix, top_k)
    return predictions


def recommendation(similarity_matrix, dataset, cutoff=[1, 3, 5, 10, 20, 50, 100], top_k=None, metrics=['accuracy', 'surprise'], split='validation'):
    """Benchmark similarity using the recommendation as a proxy task.
    The design of the recommender is based on [1].

    [1]: Piao, G., & Breslin, J. G. (2016). Measuring semantic distance for linked open data-enabled recommender systems. 
         Proceedings of the ACM Symposium on Applied Computing, 04-08-Apri, 315–320. https://doi.org/10.1145/2851613.2851839

    Args:
        similarity_matrix (np array): Similarity to benchmark
        dataset (str):
        cutoff (list, optional): Defaults to [1, 3, 5, 10, 20, 50, 100].
        top_k ([type], optional): Top-k params of the recommender. Set the number of k-NN in the user profile to be used. Defaults to None.
        metrics (list, optional): Defaults to ['accuracy', 'surprise'].
        split (str, optional): Either 'validation' or 'test'. Defaults to 'validation'.

    Returns:
        dict: performance according to the metrics and the cutoffs.
    """
    held_out = load_dataset(dataset, f'held_out_{split}')
    urm = load_dataset(dataset, 'urm')
    I = [item['id'] for item in load_dataset(dataset, 'items')]

    local_metrics = []
    global_metrics = {}
    predictions = compute_predictions(urm, similarity_matrix, top_k)

    # Mask items in the users profiles
    predictions[urm != 0] = 0

    top_n_matrix = arg_max_rows(predictions, max(cutoff))

    for row_index in range(predictions.shape[0]):
        top_n = top_n_matrix[row_index, :]
        recommendations = [I[i] for i in top_n]

        ground_truth = held_out[str(row_index)]
        results = []

        if 'accuracy' in metrics:
            accuracy = compute_accuracy_metrics(recommendations, ground_truth, cutoff)
            results.append(accuracy)

        if 'surprise' in metrics:
            # compute normalised pmi, but only once!
            try:
                normalised_pmi
            except NameError:
                normalised_pmi = (1-compute_pmi_matrix(urm))/2

            try:
                profile = np.nonzero(urm[row_index, :])[0]
                surprise = compute_surprise(top_n, profile, normalised_pmi, cutoff)
                results.append(surprise)
            except ValueError:
                logging.getLogger("recommendation").info(f"Couldn't compute surprise for user {row_index}, skipping")
                continue

            try:
                profile = np.nonzero(urm[row_index, :])[0]
                relevant_indices = np.array([i for i, e in zip(top_n, recommendations) if e in ground_truth])
                expected_surprise = compute_expected_surprise(top_n, relevant_indices, profile, normalised_pmi, cutoff)
                results.append(expected_surprise)
            except ValueError:
                logging.getLogger("recommendation").info(f"Couldn't compute expected surprise for user {row_index}, skipping")
                continue

        results_row = {k: d[k] for d in results for k in d}

        local_metrics.append(results_row)

    return local_metrics


def retrieve_similarity_matrix(algorithm, dataset, save_similarity_matrix_if_not_exists=True):
    # Load or create the similarity matrix, given an algorithm for similarity and a dataset for recommendations.
    I = [item['id'] for item in load_dataset(dataset, 'items')]
    S = I
    similarity_matrix = algorithm.similarity_matrix(S, I, save_similarity_matrix_if_not_exists=save_similarity_matrix_if_not_exists)
    return similarity_matrix
