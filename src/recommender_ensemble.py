from src.Game import Game


class RecommendationResult:
    def __init__(self, game: Game, description_similarity: float, tags_similarity: float):
        self.game = game
        self.description_similarity = description_similarity
        self.tags_similarity = tags_similarity

    @property
    def review_score(self) -> float:
        return self.game.fraction_positive_reviews
