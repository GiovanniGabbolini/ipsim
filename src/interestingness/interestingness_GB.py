from src.knowledge_graph.io import load_sub_graphs_generator
from src.data import data
import pickle
from tqdm import tqdm
import random
from src.knowledge_graph.compare_functions import *
from src.utils.utils_ngx_graph import father
from src.knowledge_graph.walk_graph import find_segues
from collections import defaultdict
import numpy as np
from src.knowledge_graph.segues_filtering import nodes_types_to_filter_loose
from src.knowledge_graph.merge_graphs import merge_graphs
from src.features.used import *
from src.knowledge_graph.segue_type import segue_type

"""
    Our interstingness
"""


_count = None


def load_count_sample():
    global _count
    if _count is None:

        with open(f"{data.preprocessed_dataset_path}/count_interestingness_GB.txt", 'rb') as f:
            _count = pickle.load(f)

        # Normalize segue_type_rarity score, as all the values are too close to 1.
        # We apply a logarithm normalization, so we:
        # 1) Compute log_2(1-rarity) for every value. This is an high number, in case rarity is close to 1, otherwise it is low;
        # 2) Consider the max over every value of the previous quantity (M);
        # 3) Divide log_2(1-rarity) by M, and get the normalized values.
        values = np.array(list(_count['segue_type_rarity'].values()))
        max_log_values = max(-np.log2(1-values))
        normalized = {k: -np.log2(1-v)/max_log_values for k, v in _count['segue_type_rarity'].items()}
        _count['segue_type_rarity'] = normalized

    return _count


def save_count_sample():
    random.seed(39)

    count = {'node': {}}
    segue_type_count = defaultdict(int)

    sub_graphs_generator = load_sub_graphs_generator(folder_name="sub_graphs_interestingness")

    goal = 5000000
    done = 0
    with tqdm(total=goal) as pbar:
        while goal-done:

            indices = (random.randint(0, len(sub_graphs_generator)-1), random.randint(0, len(sub_graphs_generator)-1))
            batches = [sub_graphs_generator[idx]() for idx in indices]

            for _ in range(len(batches[0])*10):
                done += 1
                pbar.update(1)

                g1, g2 = tuple(random.choice(b) for b in batches)
                # Segues are to be found without any kind of filter!
                # Interestingness do not involve filtering of segues, this is a step that might come afterward
                segues = find_segues(g1, g2, pre_filtering=None, post_filtering=None, nodes_types_to_filter=nodes_types_to_filter_loose)

                for segue in segues:
                    st = segue_type(segue)
                    segue_type_count[st] += 1

    total_segues = sum(segue_type_count.values())
    segue_type_count = {k: v/total_segues for k, v in segue_type_count.items()}

    max_segue_type_count = max(segue_type_count.values())
    segue_type_count = {k: v/max_segue_type_count for k, v in segue_type_count.items()}

    segue_type_rarity = {k: 1-v for k, v in segue_type_count.items()}

    count['segue_type_rarity'] = segue_type_rarity

    # From sub_graphs, we construct a unique graph
    graph = merge_graphs(sub_graphs_generator)

    for n in graph._node.values():
        in_edges = graph.in_degree(n['id'])
        out_edges = graph.out_degree(n['id'])

        if n['type'] not in count['node']:
            count['node'][n['type']] = {}

        count['node'][n['type']][n['id']] = in_edges + out_edges

    for node_type in count['node'].keys():
        v = count['node'][node_type].values()
        count['node'][node_type]['__meadian__'] = np.median(list(v))

    with open(f"{data.preprocessed_dataset_path}/count_interestingness_GB.txt", 'wb') as f:
        pickle.dump(count, f, protocol=0)


def rarity_score(segue):
    count = load_count_sample()
    st = segue_type(segue)
    if st in count['segue_type_rarity']:
        return count['segue_type_rarity'][st]
    else:
        return -np.inf


def unpopularity_score(segue):

    def _popularity_node_to_source(node):
        pop_i = []
        while node['id'] != 'source':

            id_node = node['mergiable_id']

            if node['type'] in count['node']:

                try:
                    node_edgeset = count['node'][node['type']][id_node]
                except KeyError:
                    node_edgeset = np.inf

                meadian_edgeset_actual_type = count['node'][node['type']]['__meadian__']
                pop_i.append(min(1, node_edgeset/meadian_edgeset_actual_type))

            else:
                return None

            node = father(node)

        return pop_i

    count = load_count_sample()

    pop_subpath_1 = _popularity_node_to_source(segue['n1'])
    pop_subpath_2 = _popularity_node_to_source(segue['n2'])
    if pop_subpath_1 is not None and pop_subpath_2 is not None:
        min_popularity = min(pop_subpath_1+pop_subpath_2)
        unpopularity = 1 - min_popularity
    else:
        unpopularity = -np.inf
    return unpopularity


def shortness_score(segue):
    length = 0
    for node in [segue['n1'], segue['n2']]:
        while True:
            node_father = father(node)
            generating_function = node['graph'][node_father['id']][node['id']]['generating_function']
            if generating_function == 'init':
                length += 1
                break
            func = getattr(globals()[generating_function], generating_function)
            length += 1 if 'entailed' not in func.__annotations__ else 0
            node = node_father
    shortness = 2/length
    return shortness


def interestingness(segues, rar_w, unpop_w, shortness_w):
    scores = []
    for segue in segues:
        if segue is None:
            score = 0
        else:
            rar = rarity_score(segue)
            unpop = unpopularity_score(segue)
            shortness = shortness_score(segue)
            score = rar_w*rar + unpop_w*unpop + shortness_w*shortness
        scores.append(score)
    return scores


def best_interestingness_weights():
    return {'rar_w': 0.4, 'unpop_w': 0.2, 'shortness_w': 0.4}


if __name__ == "__main__":
    save_count_sample()
