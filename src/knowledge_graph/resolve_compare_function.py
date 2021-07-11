from src.knowledge_graph.compare_functions import *
from src.utils.utils_ngx_graph import father
import copy
"""
_dict says with which function compare couple of nodes, based on their type.
It can be indexed recursively, eg: 
                                {
                                    (t1,t2):{
                                        (t3, t4): [func1],
                                        (t5, t6): [func2],
                                    }
                                }

A compare function tells wheter there is a path from two nodes or not.
The other compare function, if true, mean that there is a path among the two nodes. This happens when their value is different,
but still they have a relationships that can lead to a path among the two

Whereas nested structure are allowed, we assume to have a plain _dict, with key tuples of types that index a list of compare functions.
If we would like to avoid the association of nodes based on the type of the parents, we can discard the segues using segue filternings in the walk_graph function 
"""

# _dict is simmetric!


_dict = {
    # ('word', 'word'): [equal.equal, related_word_semantics_phrase.related_word_semantics_phrase, ],
    # ('token_phrase', 'token_phrase'): [same_word_different_sense_phrase.same_word_different_sense_phrase, ],
    # ('track_name', 'track_lyrics_without_section_tags'): [uncommon_words.uncommon_words],
    # ('album_name', 'track_lyrics_without_section_tags'): [uncommon_words.uncommon_words],
    # ('artist_name', 'track_lyrics_without_section_tags'): [uncommon_words.uncommon_words],
    # ('track_lyrics_without_section_tags', 'track_name'): [uncommon_words.uncommon_words],
    # ('track_lyrics_without_section_tags', 'album_name'): [uncommon_words.uncommon_words],
    # ('track_lyrics_without_section_tags', 'artist_name'): [uncommon_words.uncommon_words],
    # ('album_uri_spotify', 'album_uri_spotify'): [equal.equal],
    # ('artist_uri_spotify', 'artist_uri_spotify'): [equal.equal],
}


def get_dict():
    return copy.deepcopy(_dict)


def resolve_compare_function(n1, n2, d=_dict):
    if (n1['type'], n2['type']) in d:

        v = d[(n1['type'], n2['type'])]
        if type(v) == dict:
            return resolve_compare_function(father(n1), father(n2), d=v)
        elif type(v) == list:
            return d[(n2['type'], n1['type'])]
        else:
            raise TypeError("Only nested dicts or lists are allowed")

    else:
        return []
