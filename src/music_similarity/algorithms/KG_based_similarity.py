"""
Created on Sat Jan 16 2021

@author Giovanni Gabbolini
"""
from src.music_similarity.algorithms.similarity import Similarity
from src.music_similarity.dataset import load_dataset


class KGBasedSimilarity(Similarity):

    def __init__(self, dataset):
        super().__init__(dataset)
        self.graph = _Surrogate.get_instance(self.dataset).graph


class _Surrogate():

    __instance__ = None

    def __init__(self, dataset):
        if _Surrogate.__instance__ is None:
            self.graph = load_dataset(dataset, 'graph')
            _Surrogate.__instance__ = self
        else:
            raise Exception("Singleton class, use get_instance method")

    @ staticmethod
    def get_instance(dataset):
        if _Surrogate.__instance__ is None:
            _Surrogate(dataset)
        return _Surrogate.__instance__
