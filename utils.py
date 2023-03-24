import numpy as np
import pandas as pd
import sqlite3
from sentence_transformers import SentenceTransformer


def distance_between_vector_and_vectors(vector1, vectors_array):
    dot_products = np.dot(vectors_array, vector1)

    # Calculate the magnitudes of all vectors in vectors_array
    magnitudes = np.sqrt(np.sum(np.square(vectors_array), axis=1))

    # Calculate the magnitude of vector1
    magnitude_1 = np.linalg.norm(vector1)

    # Calculate the cosine similarities between vector1 and all vectors in vectors_array
    similarities = dot_products / (magnitude_1 * magnitudes)

    return similarities


def render_abstract_ranking(df, top_id) -> str:
    df = df.iloc[list(top_id)][["url", "citation"]]
    output = ""
    cnt = 0
    for idx, row in df.iterrows():
        cnt += 1
        output += "<br />" + f"[{cnt}]({row.url})" + " - " + row.citation
    return output


def calc_embeddings(ans: str = "serine is important for cancer metabolism"):
    model = SentenceTransformer("all-mpnet-base-v2")
    return model.encode(ans)


def read_dataframe_from_sqlite(db_name, table_name):
    with sqlite3.connect(db_name) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df


def get_data(data: str):
    if data == "abstract_embeddings":
        path = "data/abstracts/abstract_embeddings.csv"
        return pd.read_csv(path).drop("Unnamed: 0", axis=1).values
    
    if data == "abstract_embeddings_v2":
        path = "data/abstracts/abstract_embeddings_v2.csv"
        return pd.read_csv(path).drop("Unnamed: 0", axis=1).values

    if data == "abstracts":
        path = "data/abstracts/Book1.xlsx"
        return pd.read_excel(path)
    
    if data == "abstracts_v2":
        db_name = "collections.sqlite"
        table_name = "bioarchive_abstracts"
        return read_dataframe_from_sqlite(db_name, table_name)
