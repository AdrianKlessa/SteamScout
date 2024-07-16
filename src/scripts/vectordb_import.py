from pathlib import Path
import src.vectordb_manager
from docarray import BaseDoc
from docarray.typing import NdArray
from docarray import DocList
from vectordb import HNSWVectorDB
import pandas as pd

DESCRIPTION_DB_DIR = src.vectordb_manager.DESCRIPTION_DB_DIR
TAG_DB_DIR = src.vectordb_manager.TAG_DB_DIR

PICKLE_DIR = Path(__file__).resolve().parents[2] / "data" / "processed" / "games_with_vectors.pickle"

df = pd.read_pickle(PICKLE_DIR)


# game_id is the index in the dataframe

class GameDescriptionDoc(BaseDoc):
    game_id: int = 0
    embedding: NdArray[50]


class GameTagDoc(BaseDoc):
    game_id: int = 0
    embedding: NdArray[448]


if __name__ == "__main__":
    description_db = HNSWVectorDB[GameDescriptionDoc](workspace=DESCRIPTION_DB_DIR, space="cosine")
    tags_db = HNSWVectorDB[GameTagDoc](workspace=TAG_DB_DIR, space="cosine")
    descriptions_list = [GameDescriptionDoc(game_id=int(row['AppID']), embedding=row["Description_vector"]) for index, row in
                         df.iterrows()]
    tags_list = [GameTagDoc(game_id=int(row['AppID']), embedding=row["Tags_vector"]) for index, row in df.iterrows()]
    description_db.index(inputs=DocList[GameDescriptionDoc](descriptions_list))
    tags_db.index(inputs=DocList[GameTagDoc](tags_list))
