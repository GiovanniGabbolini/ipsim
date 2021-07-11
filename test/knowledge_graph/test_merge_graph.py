import unittest
import networkx as nx
from src.knowledge_graph.construct_graph import craft_id_node_graph
from src.knowledge_graph.merge_graphs import merge_graphs

"""
"""


class TestMergeGraph(unittest.TestCase):

    def test_merge_graph(self):
        g1 = nx.DiGraph()
        g2 = nx.DiGraph()

        g1.add_node('source', type='source', value=id(g1), id='source', graph=g1)
        g1.add_node('fn1', value='fcommon_value', type='fcommon_type', graph=g1, id='fn1')
        g1.nodes()['fn1']['mergiable_id'] = craft_id_node_graph(g1.nodes()['fn1'])
        g1.add_node('sn1', value='scommon_value', type='scommon_type', graph=g1, id='sn1')
        g1.nodes()['sn1']['mergiable_id'] = craft_id_node_graph(g1.nodes()['sn1'])
        g1.add_edge('source', 'fn1', type='fe1', generating_function='func_a')
        g1.add_edge('fn1', 'sn1', type='se1', generating_function='func_b')

        g2.add_node('source', type='source', value=id(g2), id='source', graph=g2)
        g2.add_node('fn2', value='fcommon_value', type='fcommon_type', graph=g2, id='fn2')
        g2.nodes()['fn2']['mergiable_id'] = craft_id_node_graph(g2.nodes()['fn2'])
        g2.add_node('sn2', value='scommon_value', type='scommon_type', graph=g2, id='sn2')
        g2.nodes()['sn2']['mergiable_id'] = craft_id_node_graph(g2.nodes()['sn2'])
        g2.add_edge('source', 'fn2', type='fe2', generating_function='func_a')
        g2.add_edge('fn2', 'sn2', type='se2', generating_function='func_b')

        g = merge_graphs([lambda: [g1, g2]])
        assert g.in_degree('~type:scommon_type~value:scommon_value') == 2
        assert g.out_degree('~type:fcommon_type~value:fcommon_value') == 2
        assert len(g['~type:fcommon_type~value:fcommon_value']['~type:scommon_type~value:scommon_value']) == 2
