"""
Created on --

@author Giovanni Gabbolini
"""

from nltk.corpus import wordnet as wn


def synset_attributes(synset) -> 'synset':
    """Returns the synsets attributes of a given synset, according to WordNet"""
    return [{'value': s.name()} for s in wn.synset(synset['value']).attributes()]
