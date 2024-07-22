from pathlib import Path
import sqlite3
import io
from typing import Iterable, List

import numpy as np

from Game import Game

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



# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)


def get_games_by_app_id(app_id: int) -> Iterable[Game]:
    statement = f"SELECT app_id,game_name,description,tags,positive_reviews,negative_reviews,description_vector,tags_vector FROM games WHERE app_id = ?"
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(statement, [app_id])
            return results_to_games(cursor.fetchall())
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_games_by_app_ids(app_ids: Iterable[int]) -> Iterable[Game]:
    parameter_list = list(app_ids)
    statement = f"SELECT app_id,game_name,description,tags,positive_reviews,negative_reviews,description_vector,tags_vector FROM games WHERE app_id IN (%s)"%",".join('?'*len(parameter_list))
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(statement, parameter_list)
            return results_to_games(cursor.fetchall())
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_games_by_name(name: str, exact=True, limit : int = 5, popularity_sort : bool = True) -> Iterable[Game]:
    if popularity_sort:
        order_parameter = "positive_reviews"
    else:
        order_parameter = "app_id"

    parameter = name.lower()
    if not exact:
        parameter = "%"+parameter+"%"
    if exact:
        statement = f"SELECT app_id,game_name,description,tags,positive_reviews,negative_reviews,description_vector,tags_vector FROM games WHERE LOWER(game_name) = ? ORDER BY {order_parameter} DESC LIMIT {limit}"
    else:
        statement = f"SELECT app_id,game_name,description,tags,positive_reviews,negative_reviews,description_vector,tags_vector FROM games WHERE LOWER(game_name) LIKE ? ORDER BY {order_parameter} DESC LIMIT {limit} "
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(statement,[parameter])
            res = cursor.fetchall()
            return results_to_games(res)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_games_fts(name: str, limit: int = 5) -> List[Game]:
    parameter = name.lower()
    statement = f"SELECT t1.app_id, t1.game_name, t1.description, t1.tags, t1.positive_reviews, t1.negative_reviews, t1.description_vector, t1.tags_vector FROM games t1 INNER JOIN game_titles_fts t2 ON t1.app_id = t2.app_id WHERE game_titles_fts MATCH ? ORDER BY bm25(game_titles_fts) ASC LIMIT {limit}"
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(statement,[parameter])
            res = cursor.fetchall()
            return results_to_games(res)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def results_to_games(result_list):
    results = []
    for i in result_list:
        results.append(Game(*i))
    return results
