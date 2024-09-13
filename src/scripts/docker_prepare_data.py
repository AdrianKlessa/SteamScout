from pathlib import Path
from typing import Iterable
import pandas as pd
import string
from gensim.utils import simple_preprocess
from gensim.models import doc2vec
from gensim.models.doc2vec import TaggedDocument
import numpy as np

# Define file paths

data_dir = Path(__file__).resolve().parents[2] / "data"
model_path = str(Path(__file__).resolve().parents[2] / "models" / "doc2vec_trained")
csv_path = data_dir / "raw" / "games.csv"
json_path = data_dir / "raw" / "games.json"
pickle_path = data_dir / "processed" / "games_with_vectors.pickle"

def convert_tags_from_dict(tags_dict):
    # Used for converting the .json data into the format used in the .csv file
    # i.e. dict of "Tag: tag_id" into string with comma-separated tags
    if len(tags_dict) == 0:
        return np.NaN
    key_list = list(tags_dict.keys())
    keys_string = ",".join(key_list)
    return keys_string

def read_json_dataset():
    _df = pd.read_json(json_path)
    _df = _df.T
    _df['AppID'] = _df.index
    _df.rename(columns={'name': 'Name', 'about_the_game': "About the game", "tags": "Tags", "positive": "Positive",
                        "negative": "Negative", "supported_languages": "Supported languages"}, inplace=True)

    # Workaround for compatibility with json dataset
    if isinstance(_df["Tags"].iloc[0], list):
        _df["Tags"] = _df["Tags"].apply(lambda tags: ",".join(tags))
    if isinstance(_df["Tags"].iloc[0], dict):
        _df["Tags"] = _df["Tags"].apply(lambda tags: convert_tags_from_dict(tags))
    if isinstance(_df["Supported languages"].iloc[0], list):
        _df["Supported languages"] = _df["Supported languages"].apply(lambda languages: ",".join(languages))  # ditto
    return _df


#df = pd.read_csv(csv_path)
df = read_json_dataset()

# Get games with English descriptions and train doc2vec on them
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

df = read_json_dataset()
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

# Get rows with non-empty tags and generate the tags dictionary (single tag string --> index in the embedded tag vector)
tagged_games = df[df["Tags"].notnull()].copy()
tagged_games["Tags_set"] = tagged_games["Tags"].apply(lambda x: str_tags_to_set(x))
tags_set_list = tagged_games["Tags_set"].tolist()

tags_collection = set()

for i in tags_set_list:
    tags_collection.update(i)
tag_dict = dict()
for i, el in enumerate(tags_collection):
    tag_dict[el] = i

tag_dict_len = len(tag_dict)


def vectorize_str_tags(tags: str):
    vec = np.zeros(tag_dict_len)
    if tags.lower() == "nan":
        return vec
    tags_set = str_tags_to_set(tags)
    for tag in tags_set:
        vec[tag_dict[tag]] = 1
    return vec

# Final pass - vectorize both the tags and descriptions, add as separate columns to the dataframe
df["About the game"] = df["About the game"].astype(str)
df["Tags"] = df["Tags"].astype(str)

df["Description_vector"] = df["About the game"].apply(desc_to_vector)
df["Tags_vector"] = df["Tags"].apply(vectorize_str_tags)

# Pickle and use the pickle in later steps to avoid headaches with numpy arrays in .csv file
df.to_pickle(pickle_path)
