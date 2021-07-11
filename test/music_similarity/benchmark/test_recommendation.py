import unittest
import numpy as np
from src.music_similarity.benchmark.recommendation import *
import random

"""
"""


class TestRecommendation(unittest.TestCase):

    def test_arg_max_rows(self):
        random.seed(42)
        cutoff = 30
        matrix = np.random.random((1000, 1000))

        top_n_matrix = arg_max_rows(matrix, cutoff)

        for row_index in range(matrix.shape[0]):
            top_n = top_n_matrix[row_index, :]

            for i in range(cutoff-1):
                self.assertGreaterEqual(matrix[row_index, top_n[i]], matrix[row_index, top_n[i+1]])

            for j in range(matrix.shape[1]):
                if j not in top_n:
                    self.assertGreaterEqual(matrix[row_index, top_n[-1]], matrix[row_index, j])

    def test_compute_predictions_using_top_k(self):
        # sub_test_1: when top-k is larger than the max user profile length, it should not have any effect
        random.seed(42)

        n_items = 100
        n_users = 200

        # sparisity of 10%, one every 10 possible ratings is present
        urm = np.random.binomial(1, 0.1, (n_users, n_items))
        similarity_matrix = np.random.random((n_items, n_items))
        top_k = n_items-1  # surely larger than user profile length

        p1 = compute_predictions_using_top_k(urm, similarity_matrix, top_k)
        p2 = compute_predictions(urm, similarity_matrix)
        self.assertTrue(np.allclose(p1, p2))

        # sub_test_2: toy example
        urm = np.array([
            [0, 0, 1, 1, 0],
            [1, 0, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ])
        similarity_matrix = np.hstack([np.ones((5, 1))*0, np.ones((5, 1))*0.1, np.ones((5, 1))*0.2,
                                       np.ones((5, 1))*0.3, np.ones((5, 1))*0.4])
        top_k = 2

        expected_p = np.array([
            [0.5, 0.5, 0.5, 0.5, 0.5, ],
            [0.7, 0.7, 0.7, 0.7, 0.7, ],
            [0.4, 0.4, 0.4, 0.4, 0.4, ],
            [0, 0, 0, 0, 0, ],
        ])
        p = compute_predictions_using_top_k(urm, similarity_matrix, top_k)
        self.assertTrue(np.allclose(p, expected_p))

        # sub_test_3: another toy example, but with a 1 to 5 rating urm
        urm = np.array([
            [0, 0, 1, 5, 0],
            [5, 0, 5, 1, 1],
            [0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0],
        ])
        similarity_matrix = np.hstack([np.ones((5, 1))*0, np.ones((5, 1))*0.1, np.ones((5, 1))*0.2,
                                       np.ones((5, 1))*0.3, np.ones((5, 1))*0.4])
        top_k = 2

        expected_p = np.array([
            [1.7, 1.7, 1.7, 1.7, 1.7, ],
            [0.7, 0.7, 0.7, 0.7, 0.7, ],
            [0.8, 0.8, 0.8, 0.8, 0.8, ],
            [0, 0, 0, 0, 0, ],
        ])
        p = compute_predictions_using_top_k(urm, similarity_matrix, top_k)
        self.assertTrue(np.allclose(p, expected_p))
