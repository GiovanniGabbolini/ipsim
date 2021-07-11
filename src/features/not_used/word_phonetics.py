"""
Created on --

@author Giovanni Gabbolini
"""
from abydos.phonetic import NRL


def word_phonetics(word) -> 'phonetical_representation':
    """Extracts the phonetical representation of a word using the NRL algorithm"""
    phonetical_algorithm = NRL()
    return {'value': phonetical_algorithm.encode_alpha(word['value'])}
