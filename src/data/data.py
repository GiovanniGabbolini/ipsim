'''
Created on Fri Jan 17 2020

@author Giovanni Gabbolini
'''


import pandas as pd
import os
import numpy as np
from src.data.check_file import check_file
preprocessed_dataset_path = 'res/p'
raw_dataset_path = 'res/r'
feature_path = f"{preprocessed_dataset_path}/features"
path_file_name_normalized_idf = preprocessed_dataset_path

_genres_graph = None


def genres_graph():
    path = os.path.join(preprocessed_dataset_path, 'genres_graph.npy')
    check_file('genres_graph', path)
    global _genres_graph
    if _genres_graph == None:
        _genres_graph = np.load(os.path.join(preprocessed_dataset_path,
                                             'genres_graph.npy'), allow_pickle='TRUE').item()
    return _genres_graph
