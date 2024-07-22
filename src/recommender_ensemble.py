from typing import Iterable, List

from Game import Game
import numpy as np
from numpy.linalg import norm
import vectordb_manager
import sqlite_manager

default_description_contribution = 0.5
default_tag_contribution = 1
default_score_contribution = 1


class RecommendationResult:
    def __init__(self, game: Game, description_similarity: float, tags_similarity: float, overall_score : float = 0):
        self.game = game
        self.description_similarity = description_similarity
        self.tags_similarity = tags_similarity
        self.overall_score = overall_score

    @property
    def review_score(self) -> float:
        return self.game.fraction_positive_reviews

    def __repr__(self):
        return (f"Game: {self.game}, "
                f"Overall score: {self.overall_score}"
                f"Game URL: {self.game.game_link}"
                f"Description similarity: {self.description_similarity}, "
                f"Tags similarity: {self.tags_similarity}, "
                f"review_score: {self.review_score}\n "
                )

    def to_list(self):
        return [self.game.game_name,
                "{:.2f}".format(self.overall_score * 100),
                f'<a href="{self.game.game_link}">{self.game.game_link}</a>',
                "{:.2f}".format(self.description_similarity*100),
                "{:.2f}".format(self.tags_similarity*100),
                "{:.2f}".format(self.review_score*100)
                ]

def cosine_similarity(A, B):
    all_zeros = not (np.any(A) and np.any(B))
    if all_zeros:
        return 0.0
    return (np.dot(A, B) / (norm(A) * norm(B)))


def game_pair_to_result(searched_game: Game, found_game: Game):
    doc2vec1 = searched_game.description_vector
    doc2vec2 = found_game.description_vector

    tags_1 = searched_game.tags_vector
    tags_2 = found_game.tags_vector

    doc2vec_score = cosine_similarity(doc2vec1, doc2vec2)
    tags_score = cosine_similarity(tags_1, tags_2)

    return RecommendationResult(found_game, doc2vec_score, tags_score)


def games_list_to_result(searched_game: Game, found_games: Iterable[Game]):
    return [game_pair_to_result(searched_game, i) for i in found_games]


def get_similar_games_by_description(game: Game, no_results: int) -> Iterable[Game]:
    query_vector = game.description_vector
    result_ids = vectordb_manager.find_similar_by_description_vector(query_vector, no_results + 1)
    games = sqlite_manager.get_games_by_app_ids(result_ids)
    return games


def get_similar_games_by_tags(game: Game, no_results: int) -> Iterable[Game]:
    query_vector = game.tags_vector
    result_ids = vectordb_manager.find_similar_by_tags_vector(query_vector, no_results + 1)
    games = sqlite_manager.get_games_by_app_ids(result_ids)
    return games


def get_ensemble_similar_games_by_game(game: Game, no_results: int,
                                       description_contribution: float = default_description_contribution,
                                       tags_contribution: float = default_tag_contribution,
                                       score_contribution: float = default_score_contribution) -> List[RecommendationResult]:
    description_similar_games = get_similar_games_by_description(game, no_results)
    tags_similar_games = get_similar_games_by_tags(game, no_results)

    recommended_games = description_similar_games
    # Deduplicate results
    desc_ids = [g.app_id for g in description_similar_games]
    for i in tags_similar_games:
        if i.app_id not in desc_ids:
            recommended_games.append(i)
    recommender_results = games_list_to_result(game, recommended_games)
    recommender_results.sort(reverse=True, key=lambda x: score_result(x, description_contribution, tags_contribution, score_contribution))
    return recommender_results


def score_result(recommendation_result: RecommendationResult, description_contribution: float, tags_contribution: float,
                 score_contribution: float) -> float:
    score = 0
    score += recommendation_result.description_similarity * description_contribution
    score += recommendation_result.tags_similarity * tags_contribution
    score += recommendation_result.review_score * score_contribution
    recommendation_result.overall_score = score/(description_contribution+tags_contribution+score_contribution)
    return score


def get_ensemble_similar_games_by_app_id(app_id: int, no_results: int,
                                         description_contribution: float = default_description_contribution,
                                         tags_contribution: float = default_tag_contribution,
                                         score_contribution: float = default_score_contribution) -> List[RecommendationResult]:
    game = sqlite_manager.get_games_by_app_id(app_id)[0]
    return get_ensemble_similar_games_by_game(game, no_results, description_contribution, tags_contribution,
                                              score_contribution)
