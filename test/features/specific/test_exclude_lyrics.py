import unittest
from src.features.used.track_lyrics import exclude_lyrics


class TestExcludeLyrics(unittest.TestCase):

    def test_exclude_lyrics(self):
        c = "achorusa"
        self.assertTrue(exclude_lyrics(c))
        c = "[a]chorus]a"
        self.assertTrue(exclude_lyrics(c))
        c = "[c[aa]horus]"
        self.assertTrue(exclude_lyrics(c))
        c = "[c[hook]hus]"
        self.assertTrue(exclude_lyrics(c))
        c = "[a[intro]"
        self.assertTrue(exclude_lyrics(c))
        c = "[ainTro\naaaaa]"
        self.assertFalse(exclude_lyrics(c))
        c = "[chorus]aaaaaaa"
        self.assertFalse(exclude_lyrics(c))
        c = "[chorus a$ap rocky]"
        self.assertFalse(exclude_lyrics(c))
        c = "aaa[chorus]"
        self.assertFalse(exclude_lyrics(c))
