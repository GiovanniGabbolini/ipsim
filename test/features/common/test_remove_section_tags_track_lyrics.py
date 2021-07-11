import unittest
from src.features.used.remove_section_tags_track_lyrics import remove_section_tags_track_lyrics


class TestRemoveSectionTagsTrackLyrics(unittest.TestCase):

    def test_remove_section_tags_track_lyrics(self):
        l = "[chorus]aaaa \n yeahsss  "
        self.assertEqual(remove_section_tags_track_lyrics({'value': l})['value'],
                         "aaaa \n yeahsss  ")

        l = ""
        self.assertEqual(remove_section_tags_track_lyrics({'value': l})['value'], "")
