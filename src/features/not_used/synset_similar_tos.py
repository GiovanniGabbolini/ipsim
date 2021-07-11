"""
Created on --

@author Giovanni Gabbolini
"""

from nltk.corpus import wordnet as wn


def synset_similar_tos(synset) -> 'synset':
    """Returns the member synsets similar tos of a given synset, according to WordNet"""
    return [{'value': s.name()} for s in wn.synset(synset['value']).similar_tos()]
