"""
Created on --

@author Giovanni Gabbolini
"""
from src.utils.decorator_annotations import annotations
from src.text_processing.preprocess_phrase import tokenize
from src.text_processing.preprocess_word import lower

from nltk.wsd import lesk
import threading
lock = threading.Lock()


@annotations({'entailed': True})
def token_phrase(phrase: ['track_name', 'artist_name', 'album_name', 'track_chorus'],) -> 'token_phrase':
    """Extracts a token from a phrase, that is represented as a dictionary with fields:

    * words value;
    * pos-tag;
    * sense according to Lesk word sense disambiguation algorithm.

    The edge produced by this feature is not counted in interestingess's shortness heuristics.
    """

    tokens = tokenize(phrase['value'], [lower], keep_tags=True)
    words = [t[0] for t in tokens]

    lock.acquire()
    meanings = []
    for w in words:
        meaning = lesk(words, w)
        meanings.append(meaning._name if meaning is not None else None)
    lock.release()

    return [{'value': t[0], 'pos_tag': t[1], 'meaning': m} for t, m in zip(tokens, meanings)]
