from typing import Iterable, Any
import score_color
from src.recommender_ensemble import RecommendationResult


def get_elements_from_recommendation(rec: RecommendationResult) -> Iterable[Any]:
    return [i(rec) for i in (get_game_name, get_game_score, get_game_link, get_description_score, get_tags_score, get_review_score)]

def get_game_name(rec: RecommendationResult) -> str:
    return rec.game.game_name

def get_game_score(rec: RecommendationResult) -> str:
    return f'<span style="background-color: rgb{str(score_color.get_color_for_score(rec.overall_score))}"> {rec.overall_score}</span>'

def get_game_link(rec: RecommendationResult) -> str:
    return f'<a href="{rec.game.game_link}" style="color: #0000EE;">{rec.game.game_link}</a>'

def get_description_score(rec: RecommendationResult) -> str:
    return f'<span style="background-color: rgb{str(score_color.get_color_for_score(rec.description_similarity))}"> {rec.description_similarity}</span>'

def get_tags_score(rec: RecommendationResult) -> str:
    return f'<span style="background-color: rgb{str(score_color.get_color_for_score(rec.tags_similarity))}"> {rec.tags_similarity}</span>'

def get_review_score(rec: RecommendationResult) -> str:
    return f'<span style="background-color: rgb{str(score_color.get_color_for_score(rec.review_score))}"> {rec.review_score}</span>'