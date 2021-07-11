"""
Created on Thu Mar 05 2020

@author Giovanni Gabbolini
"""
import re


def preprocess_uri_name(name):
    """given a name of an entity, it returns the name of that entity as it would be formatted as it was a name in dbpedia
       by formatted we mean that: - every letter of words separated by a space or a dash are capital. All the other are not
                                  - special characters follow the dbpedia encoding rules: https://wiki.dbpedia.org/uri-encoding

    Arguments:
        name {str} -- entity name

    Returns:
        str -- formatted entity name
    """
    words = [t for t in re.split('[ -]', name) if t != '']
    separators = [t for t in re.split('[^ -]', name) if t != '']

    words_first_capital = []
    for w in words:
        word_first_capital = w[0].upper() if w[0].isalpha() else w[0]
        word_first_capital += w[1:]
        words_first_capital.append(word_first_capital)

    name_capitalized = words_first_capital[0]
    for w, s in zip(words_first_capital[1:], separators):
        name_capitalized += s + w

    name_preprocessed = '_'.join(name_capitalized.split(' '))

    # following dbpedia encoding rules
    name_preprocessed = name_preprocessed.replace('"', '%22')

    return name_preprocessed
