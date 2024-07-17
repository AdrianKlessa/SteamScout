import gradio as gr
import sqlite_manager
import recommender_ensemble
import pandas as pd




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
    game_id = sqlite_manager.get_games_by_name(text, exact=False)[0].app_id
    print(f"Game id: {game_id}")
    results = recommender_ensemble.get_ensemble_similar_games_by_app_id(app_id=game_id, no_results=30)
    print("Found recommendations!")

    return pd.DataFrame([gamerec.to_list() for gamerec in results],
                        columns=["Game name", "Description score", "Tags score", "Review score", "Store link"])


with gr.Blocks() as app:
    gr.Markdown("Start typing below and then click **Run** to see the output.")
    with gr.Row():
        input_text = gr.Textbox(placeholder="Game name (press enter to search)",
                                label="Game search by name (press enter to search)")
    with gr.Row():
        input_dropdown = gr.Dropdown(choices=[], interactive=True, label="Select")
        select_button = gr.Button(label="Search")
    output_dataframe = gr.Dataframe(label="Similar games:",
                                    value=pd.DataFrame(),
                                    datatype=["markdown", "markdown", "markdown","markdown","html"])

    input_text.submit(fn=game_change, inputs=[input_text], outputs=[input_dropdown])
    select_button.click(fn=find_similar_games, inputs=[input_dropdown], outputs=[output_dataframe])

app.launch()
