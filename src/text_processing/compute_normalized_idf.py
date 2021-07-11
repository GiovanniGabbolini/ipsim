
'''
Created on Sat Feb 01 2020

@author Giovanni Gabbolini
'''


from nltk.tokenize import sent_tokenize
from src.text_processing.preprocess_phrase import tokenize
from src.text_processing.preprocess_word import lower
import itertools
import math
from tqdm import tqdm


def compute_normalized_idf(corpus):
    """compute the normalized idf

    Arguments:
        corpus {list of string} -- every elem of the list contains a document, in string format
    """
    d = {}
    for document in tqdm(corpus):
        words_document = []
        try:
            for p in sent_tokenize(document):
                words_document.append(tokenize(p, [lower]))
        except TypeError:
            continue
        words_document = list(itertools.chain(*words_document))
        for w in words_document:
            d[w] = d[w]+1 if w in d else 1
    N = len(d.keys())
    return {w: math.log(N/d[w])/math.log(N) for w in d.keys()}
