'''
Created on Tue Jan 28 2020

@author Giovanni Gabbolini
'''

import numpy as np
import os
from src.data import data
import pandas as pd


def create_feature(d):
    """given a df shaped in this way:
       first column: id
       second column: feature
       this method saves it as a dictionary and as a csv.
    """
    keys = list(d.keys())
    name = keys[1]
    path = os.path.join(
        data.feature_path, name)
    df = pd.DataFrame(d)
    df.to_csv('{}.csv'.format(path), index=False)
    d = dict(zip(d[keys[0]], d[keys[1]]))
    np.save('{}.npy'.format(path), d)
