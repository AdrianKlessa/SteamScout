from game_filtering import include_tag, exclude_tag
from Game import Game
from recommender_ensemble import RecommendationResult
import unittest


class TestTagsFiltering(unittest.TestCase):
    game1 = RecommendationResult(Game(0,
                                      "Racing game",
                                      "a racing game",
                                      "Racing,Sports,Driving",
                                      10,
                                      10,
                                      None,
                                      None), 0, 0, 0)

    game2 = RecommendationResult(Game(1,
                                      "WW2 FPS",
                                      "A WW2 shooter",
                                      "FPS,World War,Shooter",
                                      10,
                                      10,
                                      None,
                                      None), 0, 0, 0)
    game3 = RecommendationResult(Game(2,
                                      "WW3 FPS",
                                      "A WW3 shooter",
                                      "FPS,World War,Shooter,Futuristic",
                                      10,
                                      10,
                                      None,
                                      None), 0, 0, 0)

    def test_include_tags(self):
        games = [self.game1, self.game2, self.game3]
        filtered = include_tag(games, "World War")
        self.assertNotIn(self.game1, filtered)
        self.assertIn(self.game2, filtered)
        self.assertIn(self.game3, filtered)

    def test_exclude_tags(self):
        games = [self.game1, self.game2, self.game3]
        filtered = exclude_tag(games, "FPS")
        self.assertIn(self.game1, filtered)
        self.assertNotIn(self.game2, filtered)
        self.assertNotIn(self.game3, filtered)
