import logging
from tqdm import tqdm
import numpy as np
from src.knowledge_graph.construct_graph import construct_graph
import os
from src.data.data import preprocessed_dataset_path


def save_sub_graphs(l, start_from_batch=0, folder_name="sub_graphs_interestingness"):
    """Build and saves a number of sub-graphs, using the method construct_graph.
       The construction happens in batch

    Args:
        l (list): list of dictionaries containing entity keys
        start_from_batch (int, optional): Defaults to 0.
        folder_name (str, optional): Defaults to "sub_graphs_interestingness".

    """
    logging.getLogger('root.features').setLevel(logging.ERROR)

    batch_size = 100

    batch_n = -1
    sub_graphs = []
    for idx, d in tqdm(enumerate(l)):

        if idx % batch_size == 0:
            batch_n += 1

        if batch_n >= start_from_batch:

            g = construct_graph(d)

            sub_graphs.append(g)

            if len(sub_graphs) == batch_size:
                np.save(f"{preprocessed_dataset_path}/{folder_name}/{batch_n}", sub_graphs)
                sub_graphs = []

    if len(sub_graphs) > 0:
        np.save(f"{preprocessed_dataset_path}/{folder_name}/{batch_n}", sub_graphs)


def load_sub_graphs_generator(folder_name="sub_graphs_interestingness"):
    """Returns a generator list able to read all the graphs saved in batches by save_sub_graphs in a given folder.
    Every element of the generator is a lambda expression, that, if called, returns the corresponding batch.

    Args:
        folder_name (str, optional): Defaults to "sub_graphs_interestingness".

    Returns:
        [list]
    """

    def _get_generator(idx, folder_name):
        return lambda: list(np.load(f"{preprocessed_dataset_path}/{folder_name}/{idx}.npy", allow_pickle=True))

    sub_graphs_generator = []
    idx = 0
    while os.path.exists(f"{preprocessed_dataset_path}/{folder_name}/{idx}.npy"):
        sub_graphs_generator.append(_get_generator(idx, folder_name))
        idx += 1

    return sub_graphs_generator


def load_sub_graphs(folder_name="sub_graphs_interestingness", n_batches=-1):
    """Read back the graphs saved in batch by the former method.

    Args:
        folder_name (str, optional)
        n_batches (int, optional): Specify the number of files (or batches) that should be read. If -1, read all the files in the directory

    Returns:
        [list]: list of subgraphs ready to use
    """
    idx = 0
    sub_graphs = []
    while True:
        try:
            batch_sub_graphs = np.load(f"{preprocessed_dataset_path}/{folder_name}/{idx}.npy", allow_pickle=True)
            sub_graphs += list(batch_sub_graphs)
            idx += 1

            if idx == n_batches:
                break

        except FileNotFoundError:
            break
    return sub_graphs
