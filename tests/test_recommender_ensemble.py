import unittest
from unittest.mock import patch, MagicMock
from Game import Game
import numpy as np

"""
Cosine similarity

Searched vector:
[1.0, 1.0]

Similarity to others:

[1.0, 0.5] #0.948
[1.0, 0.4] #0.919
[0.3, 1.0] #0.880
[-0.2, 1.0] #0.554

"""


class TestRecommenderEnsemble(unittest.TestCase):
    game_0_vector = np.array([1.0, 1.0])
    game_1_vector = np.array([1.0, 0.5])
    game_2_vector = np.array([1.0, 0.4])
    game_3_vector = np.array([0.3, 1.0])
    game_4_vector = np.array([-0.2, 1.0])

    # Importing patched versions within the test to prevent initializing the DB modules
    @patch('recommender_ensemble.vectordb_manager')
    @patch('recommender_ensemble.sqlite_manager')
    def test_get_ensemble_similar_games_by_game(self, mock_sqlite_manager, mock_vectordb_manager):
        mock_vectordb_instance = MagicMock()
        mock_sqlite_instance = MagicMock()
        mock_vectordb_manager.return_value = mock_vectordb_instance
        mock_sqlite_manager.return_value = mock_sqlite_instance

        number_results = 2

        searched_game = Game(0,
                             "Searched game",
                             "Game description",
                             "tag1,tag2",
                             100,
                             50,
                             self.game_0_vector,
                             self.game_0_vector)

        found_game_1 = Game(1,
                            "Found game 1",
                            "Game description",
                            "tag1,tag2",
                            100,
                            50,
                            self.game_3_vector,
                            self.game_3_vector)

        found_game_2 = Game(2,
                            "Found game 2",
                            "Game description",
                            "tag1,tag2",
                            100,
                            50,
                            self.game_1_vector,
                            self.game_1_vector)

        found_game_3 = Game(3,
                            "Found game 3",
                            "Game description",
                            "tag1,tag2",
                            100,
                            50,
                            self.game_2_vector,
                            self.game_2_vector)

        found_game_4 = Game(4,
                            "Found game 4",
                            "Game description",
                            "tag1,tag2",
                            100,
                            50,
                            self.game_4_vector,
                            self.game_4_vector)

        mock_vectordb_manager.find_similar_by_description_vector.return_value = [1, 2]
        mock_vectordb_manager.find_similar_by_tags_vector.return_value = [3, 4]
        mock_sqlite_manager.get_games_by_app_ids.return_value = [found_game_1, found_game_2, found_game_3, found_game_4]
        mock_sqlite_manager.get_games_by_app_id.return_value = [found_game_1]

        from recommender_ensemble import get_ensemble_similar_games_by_game
        recommendation_results = get_ensemble_similar_games_by_game(searched_game, number_results, 0.5, 1.0, 1.0)

        # Check that all results are used
        self.assertEqual(4, len(recommendation_results))

        # Check order of recommendations (descending with scores)
        self.assertEqual(2, recommendation_results[0].game.app_id)
        self.assertEqual(3, recommendation_results[1].game.app_id)
        self.assertEqual(1, recommendation_results[2].game.app_id)
        self.assertEqual(4, recommendation_results[3].game.app_id)

        # Check calculated scores
        first_recommendation = recommendation_results[0]
        self.assertAlmostEqual(0.948, first_recommendation.tags_similarity, places=2)
        self.assertAlmostEqual(0.948, first_recommendation.description_similarity, places=2)
        self.assertAlmostEqual(100 / 150, first_recommendation.review_score)  # Review score as fraction of positive
        self.assertAlmostEqual((0.948 * 0.5 + 0.948 + 100 / 150) / 2.5, first_recommendation.overall_score,
                               places=2)  # Weighted score

        # Check that vectordb is called
        mock_vectordb_manager.find_similar_by_description_vector.assert_called_once_with(self.game_0_vector,
                                                                                         number_results + 1)
        mock_vectordb_manager.find_similar_by_tags_vector.assert_called_once_with(self.game_0_vector,
                                                                                  number_results + 1)
