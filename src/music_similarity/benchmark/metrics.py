import math
import numpy as np


def aggregate_metrics(l):
    """Aggregate list of metrics computed by compute metrics

    Args:
        l (list)

    Returns:
        dict
    """
    for d in l[1:]:
        assert list(l[0].keys()) == list(d.keys()), "All the dictionaries should have the same keys"
    return {key: sum(d[key] for d in l)/len(l) for key in l[0].keys()}


def compute_accuracy_metrics(predicted, ground_truth, cutoff):
    """Compute metrics that measure the quality of a predicted list with respect to the ground_truth.

    Args:
        predicted (list of strings): List of predicted objects
        ground_truth (list of strings): List of true similar objects
        cutoff (list or int)

    Returns:
        dict
    """
    cutoff = [cutoff] if type(cutoff) == int else cutoff
    assert len(predicted) >= max(cutoff), "Predicted top-n list should be larger in size that largest cutoff."

    d = {}
    for c in cutoff:
        # precision
        precision = len(set(predicted[:c]) & set(ground_truth))/c
        d[f'precision @{c}'] = precision
        # ndcg
        idcg = .0
        dcg = .0
        for i in range(c):
            relevance = 1 if predicted[i] in ground_truth else 0
            dcg += (2**relevance - 1)/math.log2(2+i)
            idcg += 1/math.log2(2+i)
        d[f'ndcg @{c}'] = dcg/idcg
    return d


def compute_pmi_matrix(urm):
    """Compute Normalised Point-wise Mutual Information (PMI) between items in urm.
    PMI is used to define surprise in [1, chapter 7.1.2].

    [1]: Kaminskas, Bridge: Diversity, Serendipity, Novelty, and Coverage: A Survey and Empirical Analysis of Beyond-Accuracy Objectives in Recommender Systems, 2017

    Args:
        urm (numpy array)
    """
    U = urm.shape[0]
    a = np.copy(urm).astype(np.float32)
    a[np.nonzero(a)] = 1
    p_ij = np.dot(a.T, a)/U
    p_i = np.count_nonzero(urm, axis=0)/U
    p_i = p_i[:, np.newaxis]
    p_i_p_j = np.dot(p_i, p_i.T)
    pmi = np.zeros((urm.shape[1], urm.shape[1]))
    pmi[p_ij != 0] = np.log2(p_ij[p_ij != 0]/(p_i_p_j[p_ij != 0]))/(-np.log2(p_ij[p_ij != 0]))
    pmi[p_ij == 0] = -1
    return pmi


def compute_surprise(predicted_indices, profile, normalised_pmi, cutoff):
    """Compute the surprise of the recommendations for a user with respect to its profile. We use the definition of surprise as presented in [1, chapter 7.1.2].
    In particular, this is the co-occurrence version of surprise.

    [1]: Kaminskas, Bridge. Diversity, Serendipity, Novelty, and Coverage: A Survey and Empirical Analysis of Beyond-Accuracy Objectives in Recommender Systems, 2017

    Args:
        predicted_indices (numpy array): indices of the predicted items as ordered in urm
        profile (numpy array): indices of items in the user profile
        normalised_pmi (numpy array): normalised pmi. In practice, is the output of compute_pmi_matrix, but normalised between 0 and 1
        cutoff (list):
    """
    a = normalised_pmi[predicted_indices, :][:, profile]
    surprise = np.min(a, axis=1)

    d = {}
    for c in cutoff:
        d[f'surprise @{c}'] = np.average(surprise[:c])

    return d


def compute_expected_surprise(predicted_indices, relevant_indices, profile, normalised_pmi, cutoff):
    """Compute the expect surprise of the recommendations for a user with respect to its profile.
    We use the definition of expected surprise as presented in [2, equation 2.12], but using co-occurence based surprise from [1, chapter 7.1.2].
    In particular, this is the co-occurrence version of surprise.

    [1]: Kaminskas, Marius; Bridge, Derek. Diversity, Serendipity, Novelty, and Coverage: A Survey and Empirical Analysis of Beyond-Accuracy Objectives in Recommender Systems, 2017.
    [2]: Carraro, Diego. PhD, 2021.

    Args:
        predicted_indices (numpy array): indices of the predicted items as ordered in urm
        relevant_indices (numpy array): indices of the relevant items held-out from train urm
        profile (numpy array): indices of items in the user profile
        normalised_pmi (numpy array): normalised pmi. In practice, is the output of compute_pmi_matrix, but normalised between 0 and 1
        cutoff (list):
    """
    a = np.zeros((len(predicted_indices), len(profile)))
    mask = np.in1d(predicted_indices, relevant_indices)
    if np.any(mask):
        a[mask] = normalised_pmi[relevant_indices, :][:, profile]
    expected_surprise = np.min(a, axis=1)

    d = {}
    for c in cutoff:
        d[f'expected surprise @{c}'] = np.average(expected_surprise[:c])

    return d
