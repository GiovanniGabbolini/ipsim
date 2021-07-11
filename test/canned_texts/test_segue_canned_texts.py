import unittest
from unittest.mock import patch, MagicMock
from src.knowledge_graph.construct_graph import construct_graph
from src.knowledge_graph.walk_graph import find_segues
from src.knowledge_graph.resolve_compare_function import get_dict
from src.canned_texts.segue_canned_texts import segue_canned_texts
from src.knowledge_graph.applicable_actions import MockedActionsSupplier


class TestSegueCannedTexts(unittest.TestCase):

    def _get_dict(self, *args):
        mocked_dict = {}

        d = get_dict()
        for k, funcs in d.items():
            funcs_mocked = []

            for func in funcs:
                func_mocked = MagicMock(return_value={'outcome': True})
                func_mocked.__name__ = func.__name__
                funcs_mocked.append(func_mocked)

            mocked_dict[k] = funcs_mocked
        return mocked_dict

    def test_segue_canned_texts(self):

        d = {
            'track_uri_spotify': 'bla',
            'track_name': 'bla',
            'artist_name': 'bla',
            'artist_uri_spotify': 'bla',
            'album_name': 'bla',
            'album_uri_spotify': 'bla',
        }

        g = construct_graph(d, supplier=MockedActionsSupplier())

        segues = find_segues(g, g, pre_filtering=lambda a, b: True, post_filtering=lambda a, b, c: True, d=self._get_dict())

        # descr
        for d in segues:
            t = segue_canned_texts(d, 'description', excecute_code=False)

        # lines
        for d in segues:
            t = segue_canned_texts(d, 'line', excecute_code=False)

        # short
        for d in segues:
            t = segue_canned_texts(d, 'short', excecute_code=False)
