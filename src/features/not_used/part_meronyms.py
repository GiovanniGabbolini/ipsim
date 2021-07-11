"""
Created on --

@author Giovanni Gabbolini
"""

from nltk.corpus import wordnet as wn


def part_meronyms(synset) -> 'synset':
    """Returns the part meronym synsets of a given synset, according to WordNet"""
    return [{'value': s.name()} for s in wn.synset(synset['value']).part_meronyms()]
