from typing import Iterable
from recommender_ensemble import RecommendationResult


def str_tags_to_set(tags: str) -> Iterable[str]:
    return set(tags.lower().split(","))


def exclude_tag(games: Iterable[RecommendationResult], tag: str) -> Iterable[RecommendationResult]:
    filtered_games = []
    for rec in games:
        game_tags = str_tags_to_set(rec.game.tags)
        if tag.lower() not in game_tags:
            filtered_games.append(rec)
    return filtered_games


def include_tag(games: Iterable[RecommendationResult], tag: str) -> Iterable[RecommendationResult]:
    filtered_games = []
    for rec in games:
        game_tags = str_tags_to_set(rec.game.tags)
        if tag.lower() in game_tags:
            filtered_games.append(rec)
    return filtered_games


def no_adult_content(games: Iterable[RecommendationResult]) -> Iterable[RecommendationResult]:
    return exclude_tag(games, "sexual content")


def less_than_n_reviews(games: Iterable[RecommendationResult], n_reviews) -> Iterable[RecommendationResult]:
    filtered_games = []
    for rec in games:
        if rec.game.number_of_reviews < n_reviews:
            filtered_games.append(rec)
    return filtered_games
