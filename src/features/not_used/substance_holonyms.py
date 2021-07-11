"""
Created on --

@author Giovanni Gabbolini
"""

from nltk.corpus import wordnet as wn


def substance_holonyms(synset) -> 'synset':
    """Returns the substance holonyms synsets of a given synset, according to WordNet"""
    return [{'value': s.name()} for s in wn.synset(synset['value']).substance_holonyms()]
