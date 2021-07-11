"""
Created on Sat Jan 16 2021

@author Giovanni Gabbolini
"""

import numpy as np
import os
import logging
from tqdm import tqdm
from src.music_similarity.algorithms.KG_based_similarity import KGBasedSimilarity
from src.knowledge_graph.walk_graph import find_segues
from src.interestingness.interestingness_GB import best_interestingness_weights, rarity_score, unpopularity_score, shortness_score
from src.knowledge_graph.segues_filtering import nodes_types_to_filter_loose
from src.knowledge_graph.segue_type import segue_type
from src.data.data import preprocessed_dataset_path


def best_params_facebook_recommender(segues_interestingness_raw):
    # according to grid search
    segues_interestingness_refined = [i[0]*0.9 + i[1]*0 + i[2]*0.1 for i in segues_interestingness_raw]
    return sum([i for i in segues_interestingness_refined if i != -np.inf])


def best_params_lastfm_recommender(segues_interestingness_raw):
    # according to grid search
    segues_interestingness_refined = [e for e in segues_interestingness_raw if e[3] <= 15 and e[0] != -np.inf and e[1] != -np.inf]
    segues_interestingness_refined = [i[0]*0 + i[1]*0 + i[2]*1 for i in segues_interestingness_refined]
    return sum(segues_interestingness_refined)


def best_params_lastfm_similarity(segues_interestingness_raw):
    # according to grid search
    segues_interestingness_refined = [e for e in segues_interestingness_raw if e[3] <= 15 and e[0] != -np.inf and e[1] != -np.inf]
    segues_interestingness_refined = [i[0]*0 + i[1]*0.1 + i[2]*0.9 for i in segues_interestingness_refined]
    return sum(segues_interestingness_refined)


def best_params_mirex_similarity(segues_interestingness_raw):
    # according to grid search
    segues_interestingness_refined = [i[0]*0.3 + i[1]*0.1 + i[2]*0.6 for i in segues_interestingness_raw if i[3] <= 15]
    return sum([i for i in segues_interestingness_refined if i != -np.inf])


def count_segues(segues_interestingness_raw):
    return len(segues_interestingness_raw)


class SegueBasedSimilarity(KGBasedSimilarity):

    def __init__(self, dataset, aggregation_strategy):
        """
        Args:
            dataset (str):
            aggregation_strategy (func): strategy for computation of similarity between two subgraphs;
        """
        super().__init__(dataset)
        self.aggregation_strategy = aggregation_strategy
        self.chunk_size = 100

    def name(self):
        return f'ipsim_{self.aggregation_strategy.__name__}'

    def compute_similarity_matrix(self, S, I):
        """Segue-based similarity works by leveraging segues between items in S and in I.
        In particular, such segues are aggregate by the aggregation_strategy.

        The segues are retrieved by the method segues_matrix. Notice that segues are asked to segues_matrix in chunk, in order to save memory.
        The chunk size is fixed and shared.
        """
        scores = np.zeros((len(S), len(I)), dtype=np.float32)
        S_in_chunks = [S[i:i+self.chunk_size] for i in range(0, len(S), self.chunk_size)]

        for idx_chunk, S_chunk in enumerate(S_in_chunks):
            segues = self.segues_matrix(S_chunk, I, idx_chunk)
            for s in range(len(S_chunk)):
                idx_row = s + idx_chunk * self.chunk_size
                for idx_col in range(len(I)):
                    if len(segues[s][idx_col]):
                        similarity = self.aggregation_strategy(segues[s][idx_col])
                        scores[idx_row, idx_col] = similarity
                    else:
                        scores[idx_row, idx_col] = 0

        return scores

    def segues_matrix(self, S_chunk, I, idx_chunk):
        path = f"{preprocessed_dataset_path}/similarity/{self.dataset}/segues_matrix"
        os.makedirs(path, exist_ok=True)

        try:
            segues_matrix_chunk = np.load(f"{path}/{idx_chunk}.npy", allow_pickle=True)
        except FileNotFoundError:
            logging.getLogger('similarity_matrix').info(
                f"Algorithm {self.name()}, cannot load chunk {idx_chunk} of segues matrix matrix, computing it ...")
            segues_matrix_chunk = [[None]*len(I) for _ in range(len(S_chunk))]
            for s in tqdm(range(len(S_chunk))):
                for k in range(len(I)):
                    if S_chunk[s] == I[k]:
                        segues_matrix_chunk[s][k] = []
                    else:
                        segues = find_segues(self.graph.nodes()[S_chunk[s]]['graph'], self.graph.nodes()[I[k]]['graph'],
                                             pre_filtering=None, post_filtering=None, nodes_types_to_filter=nodes_types_to_filter_loose)
                        segues_matrix_chunk[s][k] = [(rarity_score(segue), unpopularity_score(segue),
                                                      shortness_score(segue), len(segue_type(segue))) for segue in segues]
            np.save(f"{path}/{idx_chunk}.npy", segues_matrix_chunk)
            logging.getLogger('similarity_matrix').info(f"Algorithm {self.name()}: saved chunk {idx_chunk} of segues matrix matrix.")

        return segues_matrix_chunk
