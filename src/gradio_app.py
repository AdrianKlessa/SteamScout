from typing import Iterable

import gradio as gr
import sqlite_manager
import recommender_ensemble
from recommender_ensemble import RecommendationResult
import pandas as pd
import game_filtering
from html_elements import get_elements_from_recommendation


def game_search(text):
    found_names = [game.game_name for game in sqlite_manager.get_games_fts(text, 20)]
    exact_find = sqlite_manager.get_games_by_name(text, exact=True)
    if len(exact_find) > 0 and exact_find[0].game_name not in found_names:
        found_names.insert(0, exact_find[0].game_name)
    return found_names


def game_change(text):
    choices = game_search(text)
    if len(choices) == 0:
        return gr.update(choices=game_search(text))
    else:
        return gr.update(choices=game_search(text), value=choices[0])


def find_similar_games(text, exclude_tag, include_tag, adult_content_filter, max_reviews):
    game_id = sqlite_manager.get_games_by_name(text, exact=True)[0].app_id
    results = recommender_ensemble.get_ensemble_similar_games_by_app_id(app_id=game_id, no_results=30)
    print(f"exclude tag: {exclude_tag}")
    print(f"include tag: {include_tag}")
    print(f"adult content filter: {adult_content_filter}")
    print(f"max reviews: {max_reviews}")
    results = filter_results(results, exclude_tag, include_tag, adult_content_filter, max_reviews)
    return pd.DataFrame([get_elements_from_recommendation(gamerec) for gamerec in results],
                        columns=["Game name", "Score", "Store link", "Description score", "Tags score", "Review score"])


def filter_results(results: Iterable[RecommendationResult], exclude_tag, include_tag, adult_content_filter,
                   max_reviews) -> Iterable[RecommendationResult]:
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


with gr.Blocks() as app:
    gr.Markdown("### Similar Games search")
    gr.Markdown("Find a game by writing its name in the search box, then pressing 'SEARCH'.")
    gr.Markdown(
        "After choosing from one of the found games in the dropdown, click 'FIND SIMILAR' to get recommendations.")

    with gr.Row():
        input_text = gr.Textbox(placeholder="Game name",
                                label="Game search by name")
        search_button = gr.Button(value="SEARCH")

    with gr.Row():
        input_dropdown = gr.Dropdown(choices=[], interactive=True, label="Select")
        select_button = gr.Button(value="FIND SIMILAR")

    gr.Markdown("#### Additional filters")
    with gr.Row():
        exclude_tag_input = gr.Textbox(placeholder="tag",
                                       label="Exclude tag",
                                       interactive=True)
        include_tag_input = gr.Textbox(placeholder="tag",
                                       label="Include tag",
                                       interactive=True)
        adult_content_filter_checkbox = gr.Checkbox(label="Exclude games with sexual content",
                                                    interactive=True)
        max_reviews_input = gr.Number(label="Max review count \n(leave at 0 to not filter)",
                                      precision=1,
                                      interactive=True)

    output_dataframe = gr.Dataframe(label="Similar games:",
                                    value=pd.DataFrame(),
                                    datatype=["markdown", "markdown", "html", "markdown", "markdown", "markdown"])

    search_button.click(fn=game_change, inputs=[input_text], outputs=[input_dropdown])
    input_text.submit(fn=game_change, inputs=[input_text], outputs=[input_dropdown])
    select_button.click(fn=find_similar_games,
                        inputs=[input_dropdown, exclude_tag_input, include_tag_input, adult_content_filter_checkbox,
                                max_reviews_input], outputs=[output_dataframe])

app.launch()
