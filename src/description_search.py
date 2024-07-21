from typing import Iterable

from gensim.utils import simple_preprocess
from gensim.models import doc2vec
import vectordb_manager
import numpy as np
import string
from pathlib import Path
from Game import Game
import sqlite_manager

model_path = Path(__file__).parent.absolute() / "../models/doc2vec_trained"

model = doc2vec.Doc2Vec.load(str(model_path))


# After some testing this doesn't seem to work well
# Document length has high impact on the results so it's hard to map user queries to game descriptions directly

def process_line(line: str) -> str:
    processed = line.translate(str.maketrans('', '', string.punctuation))
    return processed.lower()


def vectorize_query(query: str) -> np.ndarray:
    text_normalized = simple_preprocess(process_line(query))
    return model.infer_vector(text_normalized)


def get_results(query: str) -> Iterable[Game]:
    query_vector = vectorize_query(query)
    result_ids = vectordb_manager.find_similar_by_description_vector(query_vector, 10, False)
    return sqlite_manager.get_games_by_app_ids(result_ids)
