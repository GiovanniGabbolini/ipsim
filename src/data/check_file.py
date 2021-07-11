'''
Created on Sun Feb 16 2020

@author Giovanni Gabbolini
'''


import numpy as np


def check_file(obj, target_path):
    """checks if the files at the target path exists, and if not it creates it calling the right function

    Arguments:
        obj {string}
        target_path {string} -- 
    """
    if not os.path.exists(target_path):
        if obj == 'word2vec_raw_1m':
            save_1m_opt_format_embeddings(target_path)
        if obj == 'genres_graph':
            g = build_graph()
            np.save(target_path, g)
