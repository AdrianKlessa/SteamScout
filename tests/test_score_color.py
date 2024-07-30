import unittest
from score_color import get_color_for_score


class TestScoreColor(unittest.TestCase):
    def test_score_zero(self):
        score = 0.0
        expected_color = (255, 0, 0)
        self.assertEqual(expected_color, get_color_for_score(score))

    def test_score_one(self):
        score = 1.0
        expected_color = (0, 255, 0)
        self.assertEqual(expected_color, get_color_for_score(score))
