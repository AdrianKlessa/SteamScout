import gradio as gr
import sqlite_manager
import recommender_ensemble
import pandas as pd

from src.html_elements import get_elements_from_recommendation


def game_search(text):
    found_names = [game.game_name for game in sqlite_manager.get_games_by_name(text, exact=False)]
    print(found_names)
    return found_names


def game_change(text):
    choices = game_search(text)
    if len(choices) == 0:
        return gr.update(choices=game_search(text))
    else:
        return gr.update(choices=game_search(text), value=choices[0])


def find_similar_games(text):
    print(f"Finding similar games for {text}")
    game_id = sqlite_manager.get_games_by_name(text, exact=True)[0].app_id
    print(f"Game id: {game_id}")
    results = recommender_ensemble.get_ensemble_similar_games_by_app_id(app_id=game_id, no_results=30)
    print("Found recommendations!")

    return pd.DataFrame([get_elements_from_recommendation(gamerec) for gamerec in results],
                        columns=["Game name", "Score","Store link", "Description score", "Tags score", "Review score"])


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

    output_dataframe = gr.Dataframe(label="Similar games:",
                                    value=pd.DataFrame(),
                                    datatype=["markdown", "markdown","html","markdown", "markdown", "markdown"])

    search_button.click(fn=game_change, inputs=[input_text], outputs=[input_dropdown])
    input_text.submit(fn=game_change, inputs=[input_text], outputs=[input_dropdown])
    select_button.click(fn=find_similar_games, inputs=[input_dropdown], outputs=[output_dataframe])

app.launch()
