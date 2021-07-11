import unittest
from src.features.array_feature import get_feature_signature_details
from src.features.used.artist_uri_dbpedia import artist_uri_dbpedia


class TestGetFeatureSignatureDetails(unittest.TestCase):

    def test_get_feature_signature_details(self):
        feature_args_names, feature_name = get_feature_signature_details(
            artist_uri_dbpedia)
        self.assertEqual(feature_args_names, ('artist_name',))
        self.assertEqual(feature_name, 'artist_uri_dbpedia')
