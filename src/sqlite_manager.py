from pathlib import Path
import sqlite3
import io
from typing import Iterable

import numpy as np

SQLITE_PATH = Path(__file__).resolve().parent / "databases" / "main_game_db.db"


# https://stackoverflow.com/a/18622264 (unutbu)
def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


class Game:
    # Note to self: consider using attrs if more classes like this arise
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
        return str(self.__dict__)

    @property
    def fraction_positive_reviews(self) -> float:
        return self.positive_reviews / ((self.positive_reviews + self.negative_reviews))


# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)


def get_games_by_app_id(app_id: int) -> Iterable[Game]:
    statement = f"SELECT app_id,game_name,description,tags,positive_reviews,negative_reviews,description_vector,tags_vector FROM games WHERE app_id = '{app_id}'"
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            return results_to_game(cursor.fetchall())
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def get_games_by_name(name: str, exact=True) -> Iterable[Game]:
    if exact:
        statement = f"SELECT app_id,game_name,description,tags,positive_reviews,negative_reviews,description_vector,tags_vector FROM games WHERE game_name = '{name}'"
    else:
        statement = f"SELECT app_id,game_name,description,tags,positive_reviews,negative_reviews,description_vector,tags_vector FROM games WHERE game_name LIKE '%{name}%'"
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            return results_to_game(cursor.fetchall())
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def results_to_game(result_list):
    results = []
    for i in result_list:
        results.append(Game(*i))
    return results


if __name__ == "__main__":
    print(get_games_by_app_id(10)[0].fraction_positive_reviews)
    #print(results_to_dict(get_games_by_app_id(10)))
    #print(results_to_dict(get_games_by_app_id(10))[0]["description_vector"])
    #print(get_games_by_name("Counter-Strike", exact=False))
