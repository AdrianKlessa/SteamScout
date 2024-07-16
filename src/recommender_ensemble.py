from src.Game import Game
import numpy as np
from numpy.linalg import norm


class RecommendationResult:
    def __init__(self, game: Game, description_similarity: float, tags_similarity: float):
        self.game = game
        self.description_similarity = description_similarity
        self.tags_similarity = tags_similarity

    @property
    def review_score(self) -> float:
        return self.game.fraction_positive_reviews


def cosine_similarity(A, B):
    all_zeros = not (np.any(A) and np.any(B))
    if all_zeros:
        return 0.0
    return (np.dot(A, B) / (norm(A) * norm(B)))


def games_to_result(searched_game: Game, found_game: Game):
    doc2vec1 = searched_game.description_vector
    doc2vec2 = found_game.description_vector

    tags_1 = searched_game.tags_vector
    tags_2 = found_game.tags_vector

    doc2vec_score = cosine_similarity(doc2vec1, doc2vec2)
    tags_score = cosine_similarity(tags_1, tags_2)

    return RecommendationResult(found_game, doc2vec_score, tags_score)

def get_similar_games_by_description(game: Game):
    pass

def get_similar_games_by_tags(game : Game):
    pass