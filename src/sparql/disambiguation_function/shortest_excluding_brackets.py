
import re


def shortest_excluding_brackets(uris):
    """consider the shortest uri as first.
       rationale: if the uris comes all match a word, we should exclude the 
       uris which contain other names other than the one searched for

       eg: if the uris are all about "Toto", the we'd want to prefer
           Toto_(band) to Toto_Cotugno

       we can be sure that additional info are among brackets, while
       additional piece of a name of an entity are not

    Arguments:
        uris {list} --

    Returns:
        [str] -- a uri on the list
    """
    uris.sort(key=lambda x: len(
        re.sub('[\(\[].*?[\)\]]', '', x)))
    return uris[0]
