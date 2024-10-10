from typing import Sequence

import sqlite_manager
import recommender_ensemble
from recommender_ensemble import RecommendationResult
import game_filtering

requested_recommender_results = 30

def get_game_app_id_from_title(title: str) -> int:
    res = sqlite_manager.get_games_by_name(title, exact=True)
    if len(res) == 0:
        return -1
    return res[0].app_id

def game_search(text):
    """
    Find games with titles similar to the provided one. If there exists an exact match, it will be the first result.
    :param text: Title to search for
    :return: List of (game title, app_id) that were found matching the query
    """
    found_games = [{"game_name": game.game_name, "app_id": game.app_id} for game in sqlite_manager.get_games_fts(text, 20)]
    exact_find = sqlite_manager.get_games_by_name(text, exact=True)
    if len(exact_find) > 0 and exact_find[0].game_name not in found_games:
        found_games.insert(0, {"game_name": exact_find[0].game_name, "app_id": exact_find[0].app_id})
    return found_games

def find_similar_games(app_id : int, exclude_tag : str, include_tag :str, adult_content_filter : bool, max_reviews : int) -> Sequence[RecommendationResult]:
    results = []
    for i in range(1, 4):
        # Try 3 times to get more results if filtering out a lot of results
        # Room for optimization here as queries / calculations are repeated
        results = recommender_ensemble.get_ensemble_similar_games_by_app_id(app_id=app_id,
                                                                            no_results=i * requested_recommender_results)
        results = filter_results(results, exclude_tag, include_tag, adult_content_filter, max_reviews)
        if len(results) >= requested_recommender_results:
            break
    return sorted(results,key=lambda game_rec: game_rec.overall_score, reverse=True)

def filter_results(results: Sequence[RecommendationResult], exclude_tag, include_tag, adult_content_filter,
                   max_reviews) -> Sequence[RecommendationResult]:
    filtered = results
    if exclude_tag:
        filtered = game_filtering.exclude_tag(filtered, exclude_tag)
    if include_tag:
        filtered = game_filtering.include_tag(filtered, include_tag)
    if adult_content_filter:
        filtered = game_filtering.no_adult_content(filtered)
    if max_reviews and max_reviews > 0:
        filtered = game_filtering.less_than_n_reviews(filtered, int(max_reviews))
    return filtered