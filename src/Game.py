import numpy as np


class Game:
    def __init__(self, app_id: int, game_name: str, description: str, tags: str, positive_reviews: int,
                 negative_reviews: int, description_vector: np.array, tags_vector: np.array):
        self.app_id = app_id
        self.game_name = game_name
        self.description = description
        self.tags = tags
        self.positive_reviews = positive_reviews
        self.negative_reviews = negative_reviews
        self.description_vector = description_vector
        self.tags_vector = tags_vector

    def __repr__(self):
        return self.game_name

    @property
    def fraction_positive_reviews(self) -> float:
        if self.number_of_reviews == 0:
            return 0.5
        return self.positive_reviews / (self.positive_reviews + self.negative_reviews)

    @property
    def number_of_reviews(self) -> int:
        return self.positive_reviews + self.negative_reviews

    @property
    def game_link(self) -> str:
        return f'https://store.steampowered.com/app/{self.app_id}'
