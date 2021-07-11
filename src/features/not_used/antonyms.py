"""
Created on --

@author Giovanni Gabbolini
"""
from nltk.corpus import wordnet as wn


def antonyms(lemma) -> 'lemma':
    """Retrieves the antonyms of a lemma i.e. the lemmas that mean the contrary, using Word Net

    Returns:
        list: the antonym lemmas, represented as strings
    """
    return [{'value': f"{l.synset().name()}.{l.name()}"} for l in wn.lemma(lemma['value']).antonyms()]
