"""
Created on Mon Mar 02 2020

@author Giovanni Gabbolini
"""

import re


def preprocess_music_seed_key(key_value):
    """Return the key value after having removed additional info like remix, remastered ecc.

    It removes:

    * Everything in brackets, either round or square;
    * Everything after '-'.

    Arguments:
        key_value {string} -- 

    """
    preprocessed_key_value = re.sub("([\(\[]).*?([\)\]])|-.*", "", key_value).strip()
    return preprocessed_key_value
