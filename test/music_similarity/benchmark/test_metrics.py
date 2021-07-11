import unittest
import numpy as np
from src.music_similarity.benchmark.metrics import *
import random

"""
"""


class TestRecommendation(unittest.TestCase):

    def test_compute_pmi(self):
        urm = np.array([
            [1, 0, 5, 0, 1, 0],
            [0, 0, 1, 1, 1, 0],
            [3, 0, 0, 0, 0, 0],
        ])

        pmi = compute_pmi_matrix(urm)

        # pmi is symmetric
        self.assertTrue(np.allclose(
            pmi,
            pmi.T
        ))

        self.assertTrue(np.allclose(
            pmi[0, 2],
            np.log2((1/3)/(4/9))/(-np.log2(1/3))
        ))

        self.assertTrue(np.allclose(
            pmi[2, 4],
            1
        ))

        self.assertTrue(np.allclose(
            pmi[0, 3],
            -1
        ))

        self.assertTrue(np.allclose(
            pmi[1, 1],
            -1
        ))

        self.assertTrue(np.allclose(
            pmi[0, 0],
            1
        ))

        self.assertTrue(np.allclose(
            pmi[2, 5],
            -1
        ))
