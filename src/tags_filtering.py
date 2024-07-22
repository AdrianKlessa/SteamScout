from typing import Iterable
from Game import Game


def str_tags_to_set(tags: str) -> Iterable[str]:
    return set(tags.lower().split(","))


def exclude_tag(games: Iterable[Game], tag: str) -> Iterable[Game]:
    filtered_games = []
    for game in games:
        game_tags = str_tags_to_set(game.tags)
        if tag.lower() not in game_tags:
            filtered_games.append(game)
    return filtered_games


def include_tag(games: Iterable[Game], tag: str) -> Iterable[Game]:
    filtered_games = []
    for game in games:
        game_tags = str_tags_to_set(game.tags)
        if tag.lower() in game_tags:
            filtered_games.append(game)
    return filtered_games
