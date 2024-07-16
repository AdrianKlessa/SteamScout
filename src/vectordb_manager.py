from pathlib import Path
from docarray import DocList
from vectordb import HNSWVectorDB
from docarray import BaseDoc
from docarray.typing import NdArray
import sqlite_manager


class GameDescriptionDoc(BaseDoc):
    game_id: int = 0
    embedding: NdArray[50]


class GameTagDoc(BaseDoc):
    game_id: int = 0
    embedding: NdArray[448]


DESCRIPTION_DB_DIR = Path(__file__).resolve().parent / "databases" / "game_description_db"
TAG_DB_DIR = Path(__file__).resolve().parent / "databases" / "game_tag_db"

description_db = HNSWVectorDB[GameDescriptionDoc](workspace=DESCRIPTION_DB_DIR, space="cosine")
tags_db = HNSWVectorDB[GameTagDoc](workspace=TAG_DB_DIR, space="cosine")


def app_ids_from_results(res_object, ignore_first=True):
    ids = []
    if ignore_first:
        start = 1
    else:
        start = 0
    for m in res_object[0].matches[start:]:  # First item will be exact game you looked for
        ids.append(m.game_id)
    return ids


def find_similar_by_description_vector(description_vector, no_results=10, ignore_first=True):
    query = GameDescriptionDoc(text='query', embedding=description_vector)
    results = description_db.search(inputs=DocList[GameDescriptionDoc]([query]), limit=no_results)
    return app_ids_from_results(results, ignore_first)


def find_similar_by_tags_vector(tags_vector, no_results=10, ignore_first=True):
    query = GameTagDoc(text='query', embedding=tags_vector)
    results = tags_db.search(inputs=DocList[GameTagDoc]([query]), limit=no_results)
    return app_ids_from_results(results, ignore_first)


if __name__ == '__main__':
    cs_go_tags_vector = sqlite_manager.get_games_by_app_id(730)[0].tags_vector
    res = find_similar_by_tags_vector(cs_go_tags_vector, 2)
    for i in res:

        print(sqlite_manager.get_games_by_app_id(i)[0].game_name)
