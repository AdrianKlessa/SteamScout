from pathlib import Path
import sqlite3
import io
import numpy as np

SQLITE_PATH = Path(__file__).resolve().parent / "databases" / "main_game_db.db"
# TODO: Make the results into a custom object

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

def get_games_by_app_id(app_id: int):
    statement = f"SELECT app_id,game_name,description,tags,positive_reviews,negative_reviews,description_vector,tags_vector FROM games WHERE app_id = '{app_id}'"
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            return results_to_dict(cursor.fetchall())
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def get_games_by_name(name: str, exact=True):
    if exact:
        statement = f"SELECT app_id,game_name,description,tags,positive_reviews,negative_reviews,description_vector,tags_vector FROM games WHERE game_name = '{name}'"
    else:
        statement = f"SELECT app_id,game_name,description,tags,positive_reviews,negative_reviews,description_vector,tags_vector FROM games WHERE game_name LIKE '%{name}%'"
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            return results_to_dict(cursor.fetchall())
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def results_to_dict(result_list):
    results = []
    for x, el1 in enumerate(result_list):
        res_dict = dict()
        for y, el2 in enumerate(('app_id', 'game_name', 'description', 'tags', 'positive_reviews', 'negative_reviews',
                                 'description_vector', 'tags_vector')):
            res_dict[el2] = result_list[x][y]
        results.append(res_dict)
    return results


if __name__ == "__main__":
    #print(get_games_by_app_id(10))
    #print(results_to_dict(get_games_by_app_id(10)))
    #print(results_to_dict(get_games_by_app_id(10))[0]["description_vector"])
    print(get_games_by_name("Counter-Strike", exact=False))
