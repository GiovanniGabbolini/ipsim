'''
Created on Sat Feb 01 2020

@author Giovanni Gabbolini
'''


from nltk.tokenize import TweetTokenizer
from nltk import pos_tag


def tokenize(phrase, funcs_word=[], thr_length=0, tags_filter=lambda t: True, keep_tags=False):
    """Given a string, it tokenizes it and then apply funcs to words.
       It reduces the string in a series of word tokens.
       It isolates the alphanumerical characters and ignores the special ones

    Arguments:
        phrase {string} -- 
        funcs_word {list} -- funcs belonging to preprocess_word module to apply to words in the phrase
        thr_length {int} -- holds with >=
        post_tags_to_filter {set} -- function for filtering postags

    Returns:
        list -- 
    """
    r = []

    tknzr = TweetTokenizer()
    tokenized_phrase = tknzr.tokenize(phrase)

    tokenized_pos_tag_filtered_phrase = []
    tagged_sentence = pos_tag(tokenized_phrase)
    for t in tagged_sentence:
        if tags_filter(t[1]):
            tokenized_pos_tag_filtered_phrase.append(t)

    tokenized_pos_tag_and_thr_filtered_phrase = []
    for t in tokenized_pos_tag_filtered_phrase:
        if len(t[0]) >= thr_length:
            tokenized_pos_tag_and_thr_filtered_phrase.append(t)

    if len(funcs_word) > 0:
        r = []
        for t in tokenized_pos_tag_and_thr_filtered_phrase:
            for func in funcs_word:
                w = func(t[0])
            if w != '':
                r.append((w, t[1]))
    else:
        r = tokenized_pos_tag_and_thr_filtered_phrase

    if keep_tags:
        return r
    else:
        return [t[0] for t in r]
