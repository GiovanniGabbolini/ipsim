"""
Created on --

@author Giovanni Gabbolini
"""

from nltk.corpus import wordnet as wn


def member_holonyms(synset) -> 'synset':
    """Returns the member holonyms synsets of a given synset, according to WordNet"""
    return [{'value': s.name()} for s in wn.synset(synset['value']).member_holonyms()]
