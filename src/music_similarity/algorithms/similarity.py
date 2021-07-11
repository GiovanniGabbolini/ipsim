"""
Created on Sat Jan 16 2021

@author Giovanni Gabbolini
"""

import numpy as np
from src.data.data import preprocessed_dataset_path
import logging


class Similarity():

    def __init__(self, dataset):
        self.dataset = dataset

    def similarity_matrix(self, S, I, save_similarity_matrix_if_not_exists=False):
        """Compute similarity matrix with items in S on the rows and items in I on the columns.
        This is a proxy method of the base class:
            - it checks whether the similarity matrix we are looking for already exists, and if so it loads it;
            - if the similarity matrix we are looking does not exist, then call subclass method for computing it. And it can save it.

        Args:
            S (list): Seed items. Represented as ids;
            I (list): Items of which should be assessed the similarity with seed items. Represented as ids.
            save_similarity_matrix_if_not_exists (bool): whether or not to save it a similarity matrix we have computed because it didn't exist.

        Returns:
            np array of shape |S|x|I|
        """
        path = f"{preprocessed_dataset_path}/similarity/{self.dataset}/similarity_matrix_{self.name()}"
        try:
            similarity_matrix = np.load(f"{path}.npy")
            logging.getLogger('similarity_matrix').info(f"Algorithm {self.name()}, similarity matrix loaded correctly.")
        except FileNotFoundError:
            logging.getLogger('similarity_matrix').info(f"Algorithm {self.name()}, cannot load similarity matrix, computing it ...")
            similarity_matrix = self.compute_similarity_matrix(S, I)
            if save_similarity_matrix_if_not_exists:
                logging.getLogger('similarity_matrix').info(f"Algorithm {self.name()}, saving similarity matrix.")
                np.save(path, similarity_matrix)
        return similarity_matrix

    def compute_similarity_matrix(self, S, I):
        """Compute similarity matrix with items in S on the rows and items in I on the columns.

        Args:
            S (list): Seed items. Represented as ids;
            I (list): Items of which should be assessed the similarity with seed items. Represented as ids.

        Raises:
            NotImplementedError: This method should be implemented by a sub-class. If not, raises this exception.

        Returns:
            np array of shape |S|x|I|
        """
        raise NotImplementedError(f"Method compute_similarity_matrix in {self.name()} was not implemented!")

    def name(self):
        return 'base_class'


class Random(Similarity):

    def compute_similarity_matrix(self, S, I):
        return np.random.rand(len(S), len(I))

    def name(self):
        return 'random'
