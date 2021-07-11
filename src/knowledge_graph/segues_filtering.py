from src.utils.utils_ngx_graph import father, artist_name
from src.data.word_concreteness import word_concreteness
from src.text_processing.preprocess_word import stem


def _node_originating_synset(n):
    while n['type'] == 'synset':
        n = father(n)
    return n


def _node_originating_lemma(n):
    while n['type'] == 'lemma':
        n = father(n)
    return n


# Two entities cannot be joyned by a node of these types.
# The strict version filters out nodes for empirical reasons, we are not interested in showing such segues.
# The loose version filters out only the nodes directly connected to source, i.e. artist_name, ...
nodes_types_to_filter_strict = set(['artist_name', 'album_name', 'track_name', 'track_uri_spotify', 'artist_uri_spotify', 'album_uri_spotify',
                                    'musical_genre_musicbrainz_id', 'area_musicbrainz_id', 'date', 'award_wikidata',
                                    'artist_wikidata_id', 'token_phrase'])
nodes_types_to_filter_loose = set(['artist_name', 'album_name', 'track_name', 'track_uri_spotify', 'artist_uri_spotify', 'album_uri_spotify'])

_pre = {
    'word': {
        'equal': lambda n:
        # Filter out close class words
        father(n)['pos_tag'] in ['NNPS', 'NN', 'NNS', 'NNP'] and
        len(n['value']) >= 3 and
        father(father(n))['type'] in ['track_name', 'album_name', 'artist_name'] and
        word_concreteness(n['value']) > 4
    },
    'synset': {
        'equal': lambda n:
            # we keep only Nouns ..
            father(_node_originating_synset(n))['pos_tag'] in ['NNPS', 'NN', 'NNS', 'NNP'] and
            # .. longer than 2 ..
            len(_node_originating_synset(n)['value']) >= 3 and
            # .. excluding words coming from chorus ..
            father(father(_node_originating_synset(n)))['type'] in ['track_name', 'album_name', 'artist_name'] and
            # .. concrete ..
            word_concreteness(_node_originating_synset(n)['value']) > 4
    },
    'lemma': {
        'equal': lambda n:
        # We exclude close class words ..
        father(_node_originating_lemma(n))['pos_tag'] in ['NNPS', 'NN', 'NNS', 'NNP'] and
        # .. longer than 2 ..
        len(_node_originating_lemma(n)['value']) >= 3 and
        # .. excluding words coming from chorus ..
        father(father(_node_originating_lemma(n)))['type'] in ['track_name', 'album_name', 'artist_name'] and
        word_concreteness(_node_originating_lemma(n)['value']) > 4,
    },
    'stem': {
        'equal': lambda n:
        len(father(n)['value']) >= 3 and
        father(father(n))['pos_tag'] in ['NNPS', 'NN', 'NNS', 'NNP'] and
        father(father(father(n)))['type'] in ['track_name', 'album_name', 'artist_name'] and
        word_concreteness(father(n)['value']) > 4,
    },
    'phonetical_representation': {
        'equal': lambda n:
        len(father(n)['value']) >= 3,
    },
    'token_phrase': {
        # Filter out close class words
        'same_word_different_sense_phrase': lambda n:
        len(n['value']) >= 3 and
        n['pos_tag'] not in ["CC", "DT", "EX", "IN", "MD", "PDT", "PRP", "POS", "PRP$", "TO", "UH", "WDT", "WP", "WRB"],
    },
}

_post = {
    'all': lambda n1, n2: artist_name(n1['graph']) != artist_name(n2['graph']),
    ('lemma', 'lemma'): {
        'equal': lambda n1, n2: father(n1)['type'] != 'word' or father(n2)['type'] != 'word',
    },
    ('synset', 'synset'): {
        'equal': lambda n1, n2:
            stem(_node_originating_synset(n1)['value']) != stem(_node_originating_synset(n2)['value']),
    },
    ('artist_musicbrainz_id', 'artist_musicbrainz_id'): {
        'equal': lambda n1, n2:
            not(father(n1)['type'] == 'artist_name' and father(n2)['type'] == 'artist_name')
    }
}


def pre(n, func):
    """Pre-filter nodes before feeding them as input to compare functions.
       It takes as input just a node and the compare function.

       Conditions on couple of nodes can be imposed by using the post function

    Args:
        n (node):
        func (function): Compare function's name

    Returns:
        bool: True, if n should be kept. False, if it should be filtered out
    """
    if n['type'] in _pre:
        if func in _pre[n['type']]:
            return _pre[n['type']][func](n)
    return True


def post(n1, n2, func):
    """Post-filter segues, so nodes that satisfy a compare functions.

       Conditions can be given on specific couple of nodes, or can they be general (keyword all)

    Args:
        n1 (node)
        n2 (node)
        func (function): Compare function's name

    Returns:
        bool: True, if the segue should be kept. False, if it should be filtered out
    """
    if _post['all'](n1, n2):

        if (n1['type'], n2['type']) in _post:
            if func in _post[(n1['type'], n2['type'])]:
                return _post[(n1['type'], n2['type'])][func](n1, n2)
        return True

    else:
        return False
