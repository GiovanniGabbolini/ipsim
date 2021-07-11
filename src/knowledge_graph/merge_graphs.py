import networkx as nx
from tqdm import tqdm
from src.utils.utils_ngx_graph import graph_id


def merge_graphs(generators, strategy_fields_source_node=lambda g: {}, strategy_graph_id=graph_id):
    """Given many trees, merge them in a unique knowldge graph.
    The unique graph is a multigraph.

    Args:
        generators (list): list of functions. if called, they return lists of graphs
        strategy_fields_source_node (func): returns dictionary to add to source nodes added to merged graph
        strategy_graph_id (func): given a tree returns the identifier of the tree to be used in the graph.
                                  it will be possible to access the source node of the tree in the graph given than id.

    Returns:
        nx graph: merged knowledge graph
    """
    graph = nx.MultiDiGraph()

    print('Merging subgraphs ...')
    for generator in tqdm(generators):
        for g in generator():

            id_sub_graph = strategy_graph_id(g)
            assert id_sub_graph not in graph

            graph.add_node(id_sub_graph, type='source', value=id_sub_graph, id=id_sub_graph, **strategy_fields_source_node(g))

            # Element in queue represent nodes in the shape (id_node_in_subgraph, id_node_in_graph)
            q = [('source', id_sub_graph)]
            while True:

                if len(q) == 0:
                    break
                else:
                    node = q.pop(0)

                    edges = g.edges(node[0])
                    for edge in edges:

                        n = g.nodes()[edge[1]].copy()

                        old_id = n['id']
                        new_id = n['mergiable_id']

                        n.pop('id')
                        n.pop('graph')
                        graph.add_node(new_id, id=new_id, **n)

                        type_edge = g[node[0]][old_id]['type']
                        graph.add_edge(node[1], new_id, type=type_edge)

                        q.append((old_id, new_id))

    return graph
