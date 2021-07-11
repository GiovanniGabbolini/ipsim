"""
Created on --

@author Giovanni Gabbolini
"""

from nltk.corpus import wordnet as wn


def part_holonyms(synset) -> 'synset':
    """Returns the part holonyms synsets of a given synset, according to WordNet"""
    return [{'value': s.name()} for s in wn.synset(synset['value']).part_holonyms()]
