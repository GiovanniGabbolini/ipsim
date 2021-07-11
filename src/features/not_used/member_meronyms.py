"""
Created on --

@author Giovanni Gabbolini
"""

from nltk.corpus import wordnet as wn


def member_meronyms(synset) -> 'synset':
    """Returns the member meronym synsets of a given synset, according to WordNet"""
    return [{'value': s.name()} for s in wn.synset(synset['value']).member_meronyms()]
