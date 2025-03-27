import argon2
import pandas as pd
from pathlib import Path
from argon2 import PasswordHasher
import json
import sqlite3
import io
import numpy as np
import os


SQLITE_PATH = Path(__file__).resolve().parents[1] / "databases" / "main_game_db.db"
PICKLE_DIR = Path(__file__).resolve().parents[2] / "data" / "processed" / "games_with_vectors.pickle"
USERS_FILE_PATH = Path(__file__).resolve().parents[0] / "users.json"

"""
Import data from the "games_with_vectors" pickled pandas dataframe.
Expected dataframe format is as created with the add_vectors_to_dataset notebook.
Additionally insert users from the copied json file.
"""

df = pd.read_pickle(PICKLE_DIR)


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


def create_sqlite_database():
    conn = None
    try:
        conn = sqlite3.connect(SQLITE_PATH)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_game_table():
    create_statement = """
        CREATE TABLE IF NOT EXISTS games (
                app_id INTEGER PRIMARY KEY, 
                game_name text, 
                description text,
                tags text,
                positive_reviews INTEGER,
                negative_reviews INTEGER,
                description_vector array,
                tags_vector array
                
        );"""

    # create a database connection
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(create_statement)

            conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_user_table():
    create_statement = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username text NOT NULL UNIQUE,
        password_hash text NOT NULL,
    );"""
    # create a database connection
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(create_statement)
            conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def add_users():
    with open(USERS_FILE_PATH) as f:
        users_dict = json.load(f)

    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            data = []
            ph = PasswordHasher()
            query = "INSERT INTO users ('username','password_hash') VALUES (?,?)"
            for key in users_dict.keys():
                username = key
                password_hash = ph.hash(users_dict[key])
                data.append((username, password_hash))
            cursor.executemany(query, data)
            conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        # A bit hacky and definitely not optimal but likely good enough for this use case
        # Might want to either use a separate, external database for users anyway
        # Or look into implementing something like the Gutmann method as an additional exercise
        os.remove(USERS_FILE_PATH)

def insert_data():
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            data = []
            query = "INSERT INTO games ('app_id','game_name','description','tags','positive_reviews','negative_reviews','description_vector','tags_vector') VALUES (?,?,?,?,?,?,?,?)"
            for index, row in df.iterrows():
                app_id = int(row['AppID'])
                game_name = str(row['Name'])
                description = str(row['About the game'])
                tags = str(row['Tags'])
                positive_reviews = int(row['Positive'])
                negative_reviews = int(row['Negative'])
                description_vector = row["Description_vector"]
                tags_vector = row["Tags_vector"]
                data.append((app_id, game_name, description, tags, positive_reviews, negative_reviews,
                             description_vector, tags_vector))
            cursor.executemany(query, data)
            conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


# Questionable index usefulness for "LIKE %abc%" queries since they don't use sorting
def add_index():
    index_statement = "CREATE INDEX game_name_index ON games (game_name);"
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(index_statement)

            conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def clear_games_db():
    statement = "DROP TABLE IF EXISTS games;"
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(statement)

            conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def clear_users_db():
    statement = "DROP TABLE IF EXISTS users;"
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(statement)

            conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    clear_games_db()
    clear_users_db()
    create_sqlite_database()
    create_game_table()
    add_index()
    insert_data()
