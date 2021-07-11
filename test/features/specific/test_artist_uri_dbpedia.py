import unittest
from src.features.used.artist_uri_dbpedia import artist_uri_dbpedia


class TestArtistUriDbpedia(unittest.TestCase):

    def test_artist_uri_dbpedia(self):
        # Those two do not work because we do not have both those artists on
        # dbpedia. Figure out why the pages are missing!!!

        # artist_name = 'KYLE'
        # self.assertIsNone(artist_uri_dbpedia(artist_name, recreate=True))

        # artist_name = 'Khalid'
        # self.assertIsNone(artist_uri_dbpedia(artist_name, recreate=True))

        artist_name = 'Logic'
        self.assertEqual(artist_uri_dbpedia(artist_name, recreate=True),
                         '<http://dbpedia.org/resource/Logic_(musician)>')

        artist_name = 'Drake'
        self.assertEqual(artist_uri_dbpedia(artist_name, recreate=True),
                         '<http://dbpedia.org/resource/Drake_(musician)>')

        artist_name = 'Jack Johnson'
        self.assertEqual(artist_uri_dbpedia(artist_name, recreate=True),
                         '<http://dbpedia.org/resource/Jack_Johnson_(musician)>')

        artist_name = 'Andrew McMahon in the Wilderness'
        self.assertEqual(artist_uri_dbpedia(artist_name, recreate=True),
                         '<http://dbpedia.org/resource/Andrew_McMahon>')
