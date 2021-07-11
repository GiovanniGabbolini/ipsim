"""
Created on --

@author Giovanni Gabbolini
"""

from nltk.corpus import wordnet as wn


def entailment(synset) -> 'synset':
    """Returns entailed synsets of a given synset, according to WordNet"""
    return [{'value': s.name()} for s in wn.synset(synset['value']).entailments()]
