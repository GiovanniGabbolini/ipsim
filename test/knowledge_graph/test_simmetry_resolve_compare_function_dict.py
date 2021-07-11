import unittest
from src.knowledge_graph.resolve_compare_function import _dict

"""The dictionary used to assign the compare functions have as key the types of the two nodes to match
   If a couple of types is in the dictionary, also the specular couple should be there, with same list of compare functions
"""


class TestSimmetryResolveCompareFunctionDict(unittest.TestCase):

    def test_simmetry_resolve_compare_function_dict(self):
        self._rec(_dict)

    def _rec(self, d):
        for k in d.keys():
            _k = (k[1], k[0])
            self.assertTrue(_k in d)
            self.assertEqual(d[k], d[_k])

            if type(d[k]) == dict:
                self._rec(d[k])
