import unittest
from src.features.used.track_chorus import track_chorus


class TestTrackChorus(unittest.TestCase):

    def test_track_chorus(self):
        c = "[chorus]\naa\nbbbb\naa\nbbbb\naa\nbbb\n[somethingelse]\naa\naa\n[aachorusverynice   ]\nbbbb"
        self.assertEqual(track_chorus({'value': c}, recreate=True)['value'], "bbbb")

        c = "[choruses]"
        self.assertEqual(track_chorus({'value': c}, recreate=True), None)

        c = "aaa\naaa\naaaa"
        self.assertEqual(track_chorus({'value': c}, recreate=True), None)

        c = "[chorus]\naa\nbbbb\naa\nbbbb\naa\nbbb\n[somethingelse]\naa\n[aachorusverynice   ]\nbbbb\naa\n  [hook]\naa"
        self.assertEqual(track_chorus({'value': c}, recreate=True)['value'], "aa")
