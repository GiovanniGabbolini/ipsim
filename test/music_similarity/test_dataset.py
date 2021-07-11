import unittest
import numpy as np
from src.music_similarity.dataset import listening_count_to_rating

"""
"""


class TestRecommendation(unittest.TestCase):

    def test_dataset(self):
        input = np.array([[10, 0, 0, 0, 0]])
        expected_output = np.array([[5, 0, 0, 0, 0]])
        self.assertTrue(np.all(listening_count_to_rating(input) == expected_output))

        input = np.array([[0, 10, 0, 0, 0]])
        expected_output = np.array([[0, 5, 0, 0, 0]])
        self.assertTrue(np.all(listening_count_to_rating(input) == expected_output))

        input = np.array([[0, 10, 0, 0, 0], [0, 10, 0, 0, 0]])
        expected_output = np.array([[0, 5, 0, 0, 0], [0, 5, 0, 0, 0]])
        self.assertTrue(np.all(listening_count_to_rating(input) == expected_output))

        input = np.array([[0, 10, 5, 15, 20, 3, 7]])
        expected_output = np.array([[0, 3, 1, 4, 5, 1, 2]])
        self.assertTrue(np.all(listening_count_to_rating(input) == expected_output))
