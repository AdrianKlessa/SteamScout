from typing import Iterable, Any
import score_color
from recommender_ensemble import RecommendationResult


def get_elements_from_recommendation(rec: RecommendationResult) -> Iterable[Any]:
    return [i(rec) for i in
            (get_summary, get_game_score, get_game_link, get_description_score, get_tags_score, get_review_score)]


def get_summary(rec: RecommendationResult) -> str:
    return f'<b>{rec.game.game_name}</b><br>Tags: {get_tags_string(rec)}'


def get_game_score(rec: RecommendationResult) -> str:
    return f'<span style="color: rgb{str(score_color.get_color_for_score(rec.overall_score))}">&#9632; </span>{"{:.2f}".format(rec.overall_score * 100)}'


def get_game_link(rec: RecommendationResult) -> str:
    return f'<a href="{rec.game.game_link}" style="color: #0000EE;" target="_blank" rel="noopener noreferrer">{rec.game.game_link}</a>'


def get_description_score(rec: RecommendationResult) -> str:
    return f'<span style="color: rgb{str(score_color.get_color_for_score(rec.description_similarity))}">&#9632; </span>{"{:.2f}".format(rec.description_similarity * 100)}'


def get_tags_score(rec: RecommendationResult) -> str:
    return f'<span style="color: rgb{str(score_color.get_color_for_score(rec.tags_similarity))}">&#9632; </span>{"{:.2f}".format(rec.tags_similarity * 100)}'


def get_review_score(rec: RecommendationResult) -> str:
    return f'<span style="color: rgb{str(score_color.get_color_for_score(rec.review_score))}">&#9632; </span>{"{:.2f}".format(rec.review_score * 100)}'


def get_tags_string(rec: RecommendationResult) -> str:
    tags = rec.game.tags.split(",")
    tags_string = ", ".join(tags[:5])
    if tags_string.lower().strip() == "nan":
        return "N/A"
    return tags_string
