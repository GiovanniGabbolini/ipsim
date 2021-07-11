"""
Created on --

@author Giovanni Gabbolini
"""
from nltk.corpus import wordnet as wn


def synset(word) -> 'synset':
    """Take the synset associated to a word in WordNet. Since there would be many synsets in some 
    cases, we keep just the first one, which lead to strongest associations.

    Returns:
        str: 
    """
    synsets = wn.synsets(word['value'])
    # Keep just the first first sense, favouring stronger associations
    if len(synsets) > 0:
        return {'value': synsets[0].name()}
