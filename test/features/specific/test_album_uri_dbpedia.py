import unittest
from src.features.used.album_uri_dbpedia import album_uri_dbpedia
from src.features.used.artist_uri_dbpedia import artist_uri_dbpedia


class TestAlbumUriDbpedia(unittest.TestCase):

    def test_album_uri_dbpedia(self):
        artist_name = 'Chris Brown'
        album_name = 'Chris Brown'
        artist_uri = artist_uri_dbpedia(artist_name, recreate=True)
        self.assertEqual(album_uri_dbpedia(album_name, artist_uri, artist_name, recreate=True),
                         '<http://dbpedia.org/resource/Chris_Brown_(album)>')

        artist_name = 'Ed Sheeran'
        album_name = 'x'
        artist_uri = artist_uri_dbpedia(artist_name, recreate=True)
        self.assertEqual(album_uri_dbpedia(album_name, artist_uri, artist_name, recreate=True),
                         '<http://dbpedia.org/resource/X_(Ed_Sheeran_album)>')

        artist_name = 'The xx'
        album_name = 'xx'
        artist_uri = artist_uri_dbpedia(artist_name, recreate=True)
        self.assertEqual(album_uri_dbpedia(album_name, artist_uri, artist_name, recreate=True),
                         '<http://dbpedia.org/resource/Xx_(album)>')

        artist_name = 'Big Sean'
        album_name = 'I Decided.'
        artist_uri = artist_uri_dbpedia(artist_name, recreate=True)
        self.assertIsNone(album_uri_dbpedia(
            album_name, artist_uri, artist_name, recreate=True))

        artist_name = 'Phantogram'
        album_name = 'Nightlife'
        artist_uri = artist_uri_dbpedia(artist_name, recreate=True)
        self.assertEqual(album_uri_dbpedia(album_name, artist_uri, artist_name, recreate=True),
                         '<http://dbpedia.org/resource/Nightlife_(EP)>')

        artist_name = 'Blind Melon'
        album_name = 'Blind Melon'
        artist_uri = artist_uri_dbpedia(artist_name, recreate=True)
        self.assertEqual(album_uri_dbpedia(album_name, artist_uri, artist_name, recreate=True),
                         '<http://dbpedia.org/resource/Blind_Melon_(album)>')

        artist_name = 'Lynyrd Skynyrd'
        album_name = "Pronounced' Leh-'Nerd 'Skin-'Nerd"
        artist_uri = artist_uri_dbpedia(artist_name, recreate=True)
        self.assertEqual(album_uri_dbpedia(album_name, artist_uri, artist_name, recreate=True),
                         "<http://dbpedia.org/resource/(Pronounced_'Lĕh-'nérd_'Skin-'nérd)>")

        artist_name = 'JAY Z'
        album_name = 'The Black Album'
        artist_uri = artist_uri_dbpedia(artist_name, recreate=True)
        self.assertEqual(album_uri_dbpedia(album_name, artist_uri, artist_name, recreate=True),
                         '<http://dbpedia.org/resource/The_Black_Album_(Jay-Z_album)>')

        artist_name = 'Fitz and The Tantrums'
        album_name = 'Fitz and The Tantrums'
        artist_uri = artist_uri_dbpedia(artist_name, recreate=True)
        self.assertEqual(album_uri_dbpedia(album_name, artist_uri, artist_name, recreate=True),
                         '<http://dbpedia.org/resource/Fitz_and_the_Tantrums_(album)>')
