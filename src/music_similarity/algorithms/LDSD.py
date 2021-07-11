"""
Created on Sat Jan 16 2021

@author Giovanni Gabbolini
"""


from src.music_similarity.algorithms.KG_based_similarity import KGBasedSimilarity
from src.utils.utils_ngx_graph import artist_id
from tqdm import tqdm
import math
import numpy as np


class LDSD(KGBasedSimilarity):

    """LDSD algorithm for similarity of entities in KG.

    Refs:
    Passant, A. (2010). Measuring semantic distance on linking data and using it for resources recommendations. AAAI Spring Symposium - Technical Report, SS-10-07, 93–98.
    """

    def __init__(self, dataset):
        super().__init__(dataset)

    def name(self):
        return 'LDSD'

    def compute_similarity_matrix(self, S, I):
        S = [_move_from_source_node(self.graph, s) for s in S]
        I = [_move_from_source_node(self.graph, i) for i in I]
        scores = np.zeros((len(S), len(I)), dtype=np.float32)
        for idx_row in tqdm(range(len(S))):
            for idx_col in range(len(I)):
                if S[idx_row] == I[idx_col] or S[idx_row] is None or I[idx_col] is None:
                    scores[idx_row, idx_col] = 0
                else:
                    scores[idx_row, idx_col] = self._LDSD(S[idx_row], I[idx_col])
        return scores

    def _LDSD(self, r_a, r_b):
        edges_types_sprining_from_r_a = set()
        edges_types_sprining_from_r_b = set()
        for n in self.graph[r_a]:
            for k, v in self.graph.get_edge_data(r_a, n).items():
                edges_types_sprining_from_r_a.add(v['type'])
        for n in self.graph[r_b]:
            for k, v in self.graph.get_edge_data(r_b, n).items():
                edges_types_sprining_from_r_b.add(v['type'])

        a_to_b_score = 0
        b_to_a_score = 0
        incoming_score = 0
        outgoing_score = 0
        for l in edges_types_sprining_from_r_a | edges_types_sprining_from_r_b:
            a_to_b_score += (_cd(self.graph, l, r_a, r_b)/(1+math.log2(_cd_n(self.graph, l, r_a))) if _cd(self.graph, l, r_a, r_b) > 0 else 0)
            b_to_a_score += (_cd(self.graph, l, r_b, r_a)/(1+math.log2(_cd_n(self.graph, l, r_b))) if _cd(self.graph, l, r_b, r_a) > 0 else 0)

        # incoming score is always 0, the graph springs from entities I'm computing the similarity of.
        # incoming_score += (_cii(self.graph, l, r_a, r_b)/(1+math.log2(_cii_n(self.graph, l, r_a))) if _cii(self.graph, l, r_a, r_b) > 0 else 0)

        for l in edges_types_sprining_from_r_a & edges_types_sprining_from_r_b:
            cio = _cio(self.graph, l, r_a, r_b)
            outgoing_score += (cio/(1+math.log2(_cio_n(self.graph, l, r_a))) if cio > 0 else 0)

        return 1 - (1 / (1 + a_to_b_score + b_to_a_score + incoming_score + outgoing_score))


def _cio(graph, l, r_a, r_b):
    candidates_m = set([candidate_m for _, candidate_m in graph.out_edges(r_a) if _test_edge_type(graph, l, r_a, candidate_m)])
    for candidate_m in candidates_m:
        if _test_edge_type(graph, l, r_b, candidate_m):
            return 1
    return 0


_batch_candidates_rb = {}


def _cio_n(graph, l, r_a):
    v = 0
    set_r_a = set([r_a])
    candidates_m = set([candidate_m for _, candidate_m in graph.out_edges(r_a) if _test_edge_type(graph, l, r_a, candidate_m)])
    for candidate_m in candidates_m:
        if (candidate_m, l) in _batch_candidates_rb:
            candidates_r_b = _batch_candidates_rb[(candidate_m, l)]
        else:
            candidates_r_b = set([candidate_r_b for candidate_r_b, _ in graph.in_edges(
                candidate_m) if _test_edge_type(graph, l, candidate_r_b, candidate_m)])
            _batch_candidates_rb[(candidate_m, l)] = candidates_r_b

        v += len(candidates_r_b - set_r_a)
    return v


def _test_edge_type(graph, edge_type, n_1, n_2):
    """Tests whether in a direct graph, there is an edge of type edge_tyoe connecting n_1 to n_2.

    Returns:
        [bool]
    """
    d = graph.get_edge_data(n_1, n_2)
    if d:
        for k, v in d.items():
            if v['type'] == edge_type:
                return True
    return False


def _cd(graph, l, r_a, r_b):
    if r_a != r_b and _test_edge_type(graph, l, r_a, r_b):
        return 1
    else:
        return 0


def _cd_n(graph, l, r_a):
    return sum(_cd(graph, l, r_a, r_b) for r_b in graph[r_a])


def _cii(graph, l, r_a, r_b):
    candidates_m = set([candidate_m for candidate_m, _ in graph.in_edges(r_a) if _test_edge_type(graph, l, candidate_m, r_a)])
    for candidate_m in candidates_m:
        if _test_edge_type(graph, l, candidate_m, r_b):
            return 1
    return 0


def _cii_n(graph, l, r_a):
    v = 0
    candidates_m = set([candidate_m for candidate_m, _ in graph.in_edges(r_a) if _test_edge_type(graph, l, candidate_m, r_a)])
    for candidate_m in candidates_m:
        candidates_r_b = set([candidate_r_b for _, candidate_r_b in graph.out_edges(
            candidate_m) if _test_edge_type(graph, l, candidate_m, candidate_r_b)])
        for r_b in candidates_r_b:
            if r_a != r_b:
                v += 1
    return v


def _move_from_source_node(graph, source_node_id):
    """LDSD considers as similar only nodes that are either neighbors, or at distant 2 hops. All the others have similarity = 0.

    This method allows to move from source nodes to a forward node for similarity computation.
    Otherwise, from a source node there is a long road to do before reaching another source, always more than 2 hops,
    and as a result, the similarity would always be = 0.

    This method is really domain dependent from nature, and might change if the graph construction changes.

    For artist similarty, it is assumed that for every single artist we have source -> artist_name -> artist_musicbrainz_id.
    In this case, this method takes the id of the source and returns the node id of the artist_musicbrainz_id.

    Args:
        graph (nx DiGraph)
        source_node_id (str)
    """
    musicbrainz_id = artist_id(graph.nodes()[source_node_id]['graph'])
    if musicbrainz_id is None:
        return None
    else:
        son = list(graph[source_node_id])
        assert len(son) == 1
        # If the same artist name is associated to two musicbrainz ids, len(list(graph[son[0]]))>1
        # We use the musicbrainz_id of the artist to distinguish which grandson to pick.
        grandson = [i for i in list(graph[son[0]]) if musicbrainz_id in i]
        assert len(grandson) == 1
        return grandson[0]
