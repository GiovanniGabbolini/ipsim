from src.knowledge_graph.io import load_sub_graphs
from src.data import data
import pickle
from tqdm import tqdm
import json
from src.knowledge_graph.resolve_compare_function import _dict
from src.knowledge_graph.compare_functions import *
import itertools
from src.utils.utils_ngx_graph import father
import numpy as np
import networkx as nx


"""
    This file implements the paper: http://cobweb.cs.uga.edu/~budak/papers/AHARS05-Ranking-IC.pdf
"""


_count = None


def load_count_sample(variety='ksecond'):
    assert variety in ['kprime', 'ksecond', 'kderek']
    global _count

    if _count is None:
        with open(f"{data.preprocessed_dataset_path}/count_{variety}.txt", 'rb') as f:
            _count = pickle.load(f)

    return _count


def craft_id_node_graph(n):
    n_copy = n.copy()
    n_copy.pop('id')
    n_copy.pop('graph')
    s = ''
    keys = sorted(list(n_copy.keys()))
    for key in keys:
        s += f"~{key}:{n_copy[key] if type(n_copy[key])!=dict else json.dumps(n_copy[key], sort_keys=True)}"
    return s


def save_count_sample(variety='kprime'):
    assert variety in ['kprime', 'ksecond', 'kderek']

    sub_graphs = load_sub_graphs(folder_name="sub_graphs_interestingness")

    # From sub_graphs, we construct a unique graph
    graph = nx.DiGraph()

    print('Merging subgraphs ...')
    for g in tqdm(sub_graphs):

        id_sub_graph = str(id(g.nodes()['source']['graph']))
        graph.add_node(id_sub_graph, type='source', value=id_sub_graph, id=id_sub_graph)

        # Element in queue represent nodes in the shape (id_node_in_subgraph, id_node_in_graph)
        q = [('source', id_sub_graph)]
        while True:

            if len(q) == 0:
                break
            else:
                node = q.pop(0)

                edges = g.edges(node[0])
                for edge in edges:

                    n = g.nodes()[edge[1]]

                    old_id = n['id']
                    new_id = craft_id_node_graph(n)

                    n.pop('id')
                    n.pop('graph')
                    graph.add_node(new_id, id=new_id, **n)

                    generating_function = g[node[0]][old_id]['generating_function']
                    if (node[1], new_id) in graph.edges:
                        graph[node[1]][new_id]['type'].add(generating_function)
                    else:
                        graph.add_edge(node[1], new_id, type=set([generating_function]))

                    q.append((old_id, new_id))

    if variety == 'ksecond':

        def find_compare_functions_producing_additional_edges():
            """Returns all the functions that should be applied to graph to add the additional edges among entities.
               Eg: Two words can be linked by a semantic similarity edge. It is not present in graph, we should add it.

               The function equal is already included in graph: if two nodes have the same type and value, are considered the
               same in the counting!

               Viceversa, this implies that the compare function equal should be True only if the two nodes have:
               - same type
               - same value
               - no other fields other than type, value, graph and id

               Notice: if _dict is on multiple levels, this won't work, but we assume to have plain _dict.
            """
            r = []
            for k, v in _dict.items():
                if v != [equal.equal]:
                    d = {
                        'type1': k[0],
                        'type2': k[1],
                        'funcs': list(set(v)-set([equal.equal]))
                    }
                    r.append(d)
            return r

        l = find_compare_functions_producing_additional_edges()

        for d in l:

            if d['type1'] == d['type2']:
                nodes_common_type = [n for n in graph._node.values() if n['type'] == d['type1']]
                collection = itertools.combinations(nodes_common_type, 2)
            else:
                nodes_type1 = [n for n in graph._node.values() if n['type'] == d['type1']]
                nodes_type2 = [n for n in graph._node.values() if n['type'] == d['type2']]
                collection = itertools.product(nodes_type1, nodes_type2)

            for func in d['funcs']:

                print(f'Adding edges {func.__name__} among nodes of types {d["type1"]} and {d["type2"]} ...')
                for e in tqdm(collection):

                    result = func(e[0], e[1])
                    if result['outcome'] == True:

                        if (e[0]['id'], e[1]['id']) in graph.edges:
                            graph[e[0]['id']][e[1]['id']]['type'].add(func.__name__)
                        else:
                            graph.add_edge(e[0]['id'], e[1]['id'], type=set([func.__name__]))

    # Counting node rarity and popularity
    count = {
        'M': 0,  # M
        'node': {},
        'feature': {},
    }

    for n in graph._node.values():
        in_edges = graph.in_degree(n['id'])
        out_edges = graph.out_degree(n['id'])
        count['M'] += 1

        if n['type'] not in count['node']:
            count['node'][n['type']] = {'__max__': -1}

        count['node'][n['type']][n['id']] = in_edges + out_edges

        if in_edges + out_edges > count['node'][n['type']]['__max__']:
            count['node'][n['type']]['__max__'] = in_edges + out_edges

    for e in graph.edges:
        for t in graph[e[0]][e[1]]['type']:

            if t in count['feature']:
                count['feature'][t] += 1
            else:
                count['feature'][t] = 1

            count['M'] += 1

    with open(f"{data.preprocessed_dataset_path}/count_{variety}.txt", 'wb') as f:
        pickle.dump(count, f, protocol=0)


def rarity_score(segue, variety):

    def _rarity_node_to_source(node):
        rar_i = []
        M = count['M']
        g = node['graph']

        while node['id'] != 'source':

            try:
                # Subtract __max__ key
                N = len(count['node'][node['type']])-1
                rar_i.append((M-N)/M)
            except KeyError:
                return None

            # Feature step
            father_node = father(node)
            linking_feature_type = g[father_node['id']][node['id']]['generating_function']

            try:
                N = count['feature'][linking_feature_type]
                rar_i.append((M-N)/M)
            except KeyError:
                return None

            node = father_node

        return rar_i

    count = load_count_sample(variety)

    rar_subpath_1 = _rarity_node_to_source(segue['n1'])
    rar_subpath_2 = _rarity_node_to_source(segue['n2'])

    # A compare function different from equal induces another edge in the graph, which should be scored as well
    if segue['compare_function'] != 'equal':

        try:
            M = count['M']
            N = count['feature'][segue['compare_function']]
            rar_subpath_1.append((M-N)/M)
        except (KeyError, AttributeError):
            rar_subpath_1 = None

    if rar_subpath_1 is not None and rar_subpath_2 is not None:
        rarity = rar_subpath_1+rar_subpath_2
        return sum(rarity)/len(rarity)
    else:
        return -np.inf


def unpopularity_score(segue, variety):

    def _popularity_node_to_source(node):
        pop_i = []
        while node['id'] != 'source':

            id_node = craft_id_node_graph(node)

            if node['type'] in count['node']:

                try:
                    node_edgeset = count['node'][node['type']][id_node]
                except KeyError:
                    node_edgeset = 0

                max_edgeset_actual_type = count['node'][node['type']]['__max__']
                pop_i.append(node_edgeset/max_edgeset_actual_type)

            else:
                return None

            node = father(node)

        return sum(pop_i)/len(pop_i)

    count = load_count_sample(variety)

    pop_subpath_1 = _popularity_node_to_source(segue['n1'])
    pop_subpath_2 = _popularity_node_to_source(segue['n2'])
    if pop_subpath_1 is not None and pop_subpath_2 is not None:
        unpopularity = 1-(pop_subpath_1+pop_subpath_2)/2
    else:
        unpopularity = -np.inf
    return unpopularity


def shortness_score(segue):
    length_subpath_1 = len(segue['n1']['id'].split('~'))
    length_subpath_2 = len(segue['n2']['id'].split('~'))
    shortness = 1/(length_subpath_1+length_subpath_2)
    return shortness


def interestingness(segues, variety, unpop_w, shortness_w):
    assert variety in ['kprime', 'ksecond', 'kderek']
    scores = []
    for segue in segues:
        rar = rarity_score(segue, variety)
        unpop = unpopularity_score(segue, variety)
        shortness = shortness_score(segue)
        score = rar_w*rar + unpop_w*unpop + shortness_w*shortness
        scores.append(score)
    return scores
