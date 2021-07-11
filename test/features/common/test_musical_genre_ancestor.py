import unittest
from src.features.used.musical_genre_ancestor import musical_genre_ancestor


class TestGetFeatureSignatureDetails(unittest.TestCase):

    def test_musical_genre_ancestor(self):
        uri = '<http://dbpedia.org/resource/Post-punk>'
        self.assertEqual(musical_genre_ancestor(uri), ['<http://dbpedia.org/resource/Art_pop>', '<http://dbpedia.org/resource/Art_rock>', '<http://dbpedia.org/resource/Disco>',
                                                       '<http://dbpedia.org/resource/Dub_music>', '<http://dbpedia.org/resource/Electronics_in_rock_music>',
                                                       '<http://dbpedia.org/resource/Funk>', '<http://dbpedia.org/resource/Funk_rock>', '<http://dbpedia.org/resource/Glam_rock>',
                                                       '<http://dbpedia.org/resource/Jazz>', '<http://dbpedia.org/resource/Krautrock>',
                                                       '<http://dbpedia.org/resource/Musicianship_of_Brian_Wilson>', '<http://dbpedia.org/resource/Punk_rock>',
                                                       '<http://dbpedia.org/resource/Rock_music>', '<http://dbpedia.org/resource/World_music>'])
