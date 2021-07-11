
import re
from difflib import SequenceMatcher


def highest_seq_matcher_excluding_brackets(uris, ref):
    """consider that uri most similar to a string we are looking for,
       when excluding everything that there is among brackets

    Arguments:
        uris {list} --

    Returns:
        [str] -- a uri on the list
    """
    uris_p = [u.split('/')[-1] for u in uris]
    uris_p = [re.sub('[\(\[].*?[\)\]]', '', u) for u in uris_p]
    d = {t[0]: t[1] for t in zip(uris_p, uris)}
    uris_p.sort(key=lambda u: SequenceMatcher(
        None, u, ref).ratio(), reverse=True)
    return d[uris_p[0]]
