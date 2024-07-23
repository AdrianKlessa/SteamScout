from src import game_filtering
from src.Game import Game
import unittest


class TestTagsFiltering(unittest.TestCase):
    game1 = Game(0,
                 "Racing game",
                 "a racing game",
                 "Racing,Sports,Driving",
                 10,
                 10,
                 None,
                 None)

    game2 = Game(1,
                 "WW2 FPS",
                 "A WW2 shooter",
                 "FPS,World War,Shooter",
                 10,
                 10,
                 None,
                 None)
    game3 = Game(2,
                 "WW3 FPS",
                 "A WW3 shooter",
                 "FPS,World War,Shooter,Futuristic",
                 10,
                 10,
                 None,
                 None)

    def test_include_tags(self):
        games = [self.game1, self.game2, self.game3]
        filtered = game_filtering.include_tag(games, "World War")
        self.assertNotIn(self.game1, filtered)
        self.assertIn(self.game2, filtered)
        self.assertIn(self.game3, filtered)

    def test_exclude_tags(self):
        games = [self.game1, self.game2, self.game3]
        filtered = game_filtering.exclude_tag(games, "FPS")
        self.assertIn(self.game1, filtered)
        self.assertNotIn(self.game2, filtered)
        self.assertNotIn(self.game3, filtered)