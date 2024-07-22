from pathlib import Path
from typing import Iterable
import json
import pandas as pd
import string
from gensim.utils import simple_preprocess
from gensim.models import doc2vec
from gensim.models.doc2vec import TaggedDocument
import numpy as np

data_dir = Path(__file__).resolve().parents[2] / "data"
model_path = str(Path(__file__).resolve().parents[2] / "models" / "doc2vec_trained")
tags_json_path = Path(__file__).resolve().parents[2] / "notebooks" / "tag_dictionary.json"
csv_path = data_dir / "raw" / "games.csv"
pickle_path = data_dir / "processed" / "games_with_vectors.pickle"

df = pd.read_csv(csv_path)

df.dropna(subset=['Name', 'About the game'], how='any', inplace=True)
english_descriptions = df[df['Supported languages'].str.contains("English")]

pd.options.mode.chained_assignment = None
english_descriptions['About the game'] = english_descriptions['About the game'].astype(str)


def process_line(line: str) -> str:
    processed = line.translate(str.maketrans('', '', string.punctuation))
    return processed.lower()


english_descriptions['About the game'] = english_descriptions['About the game'].apply(lambda x: process_line(x))

descriptions = english_descriptions['About the game'].tolist()

train_corpus = []
for i, text in enumerate(descriptions):
    tokens = simple_preprocess(text)
    train_corpus.append(TaggedDocument(tokens, [i]))

model = doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=40)
model.build_vocab(train_corpus)

model.train(train_corpus, total_examples=model.corpus_count,
            epochs=model.epochs)  # Longer training than default because the dataset isn't large

# Adding vectors
df = pd.read_csv(csv_path)
model.save(model_path)

doc2vec_model = model


def process_line_doc2vec(line: str) -> str:
    processed = line.translate(str.maketrans('', '', string.punctuation))
    return processed.lower()


def desc_to_vector(desc: str) -> np.array:
    line = process_line_doc2vec(desc)
    line = simple_preprocess(line)
    vec = doc2vec_model.infer_vector(line)
    return vec


def str_tags_to_set(tags: str) -> Iterable[str]:
    return set(tags.split(","))


with open(tags_json_path, "r", encoding="utf-8") as f:
    tag_dict = json.load(f)


def vectorize_str_tags(tags: str):
    vec = np.zeros(448)
    if tags.lower() == "nan":
        return vec
    tags_set = str_tags_to_set(tags)
    for tag in tags_set:
        vec[tag_dict[tag]] = 1
    return vec

df["About the game"] = df["About the game"].astype(str)
df["Tags"] = df["Tags"].astype(str)

df["Description_vector"] = df["About the game"].apply(desc_to_vector)
df["Tags_vector"] = df["Tags"].apply(vectorize_str_tags)

df.to_pickle(pickle_path)
