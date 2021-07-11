"""
Created on --

@author Giovanni Gabbolini
"""

from nltk.corpus import wordnet as wn


def hyponyms(synset) -> 'synset':
    """Returns hyponyms synsets of a given synset, according to WordNet"""
    return [{'value': l.name()} for l in wn.synset(synset['value']).hyponyms()]
