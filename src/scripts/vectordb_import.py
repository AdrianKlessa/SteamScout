from pathlib import Path
from docarray import BaseDoc
from docarray.typing import NdArray
from docarray import DocList
from vectordb import HNSWVectorDB
import pandas as pd
import json

DESCRIPTION_DB_DIR = Path(__file__).resolve().parents[1] / "databases" / "game_description_db"
TAG_DB_DIR = Path(__file__).resolve().parents[1] / "databases" / "game_tag_db"

PICKLE_DIR = Path(__file__).resolve().parents[2] / "data" / "processed" / "games_with_vectors.pickle"

CONFIG_DIR = Path(__file__).resolve().parents[1] / "config.json"

df = pd.read_pickle(PICKLE_DIR)

# game_id is the index in the dataframe
DESCRIPTION_VECTOR_LENGTH = 50
TAG_VECTOR_LENGTH = df["Tags_vector"].iloc[0].size  # Set to length of first entry in df

# Store in config to avoid hardcoded vector lengths
with open(CONFIG_DIR, 'w', encoding='utf-8') as f:
    data = {"DESCRIPTION_VECTOR_LENGTH": DESCRIPTION_VECTOR_LENGTH, "TAG_VECTOR_LENGTH": TAG_VECTOR_LENGTH}
    json.dump(data, f, ensure_ascii=False, indent=4)


class GameDescriptionDoc(BaseDoc):
    game_id: int = 0
    embedding: NdArray[DESCRIPTION_VECTOR_LENGTH]


class GameTagDoc(BaseDoc):
    game_id: int = 0
    embedding: NdArray[TAG_VECTOR_LENGTH]


if __name__ == "__main__":
    description_db = HNSWVectorDB[GameDescriptionDoc](workspace=DESCRIPTION_DB_DIR, space="cosine")
    tags_db = HNSWVectorDB[GameTagDoc](workspace=TAG_DB_DIR, space="cosine")
    descriptions_list = [GameDescriptionDoc(game_id=int(row['AppID']), embedding=row["Description_vector"]) for
                         index, row in
                         df.iterrows()]
    tags_list = [GameTagDoc(game_id=int(row['AppID']), embedding=row["Tags_vector"]) for index, row in df.iterrows()]
    description_db.index(inputs=DocList[GameDescriptionDoc](descriptions_list))
    tags_db.index(inputs=DocList[GameTagDoc](tags_list))
