"""
Created on --

@author Giovanni Gabbolini
"""

from nltk.corpus import wordnet as wn


def synset_also_sees(synset) -> 'synset':
    """Returns the also sees synsets of a given synset, according to WordNet"""
    return [{'value': s.name()} for s in wn.synset(synset['value']).also_sees()]
