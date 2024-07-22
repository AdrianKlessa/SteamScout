import sqlite3
import io
import numpy as np
from pathlib import Path

SQLITE_PATH = Path(__file__).resolve().parents[1] / "databases" / "main_game_db.db"

create_virtual_table_statement = """
CREATE VIRTUAL TABLE game_titles_fts
USING fts5(app_id, game_name);
"""

add_data_statement = """
INSERT INTO game_titles_fts(app_id, game_name)
SELECT app_id, game_name FROM games;

"""

insert_trigger = """
CREATE TRIGGER insert_game_fts
after insert on games
begin
INSERT INTO game_titles_fts(app_id, game_name)
VALUES(NEW.app_id, NEW.game_name);
end;

"""

update_trigger = """
CREATE TRIGGER update_game_fts
after update on games
begin
UPDATE game_titles_fts
SET game_name = NEW.game_name
WHERE app_id = NEW.app_id;
end;
"""

delete_trigger = """
CREATE TRIGGER delete_game_fts
after delete on games
begin
DELETE FROM game_titles_fts
WHERE app_id = OLD.app_id;
end;

"""

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

def enable_fts():
    pass

if __name__ == '__main__':
    try:
        with sqlite3.connect(SQLITE_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute(create_virtual_table_statement)
            cursor.execute(add_data_statement)
            cursor.execute(insert_trigger)
            cursor.execute(update_trigger)
            cursor.execute(delete_trigger)

            conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()