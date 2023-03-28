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


def calc_embeddings(ans: str = "serine is important for cancer metabolism", model_name:str='bert'):
    if model_name == 'bert':
        model = SentenceTransformer("all-mpnet-base-v2")
    elif model_name == 'sci-bert':
        model = SentenceTransformer("allenai/scibert_scivocab_uncased")
    else:
        1/0
    return model.encode(ans)


def read_dataframe_from_sqlite(db_name, table_name):
    with sqlite3.connect(db_name) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df

def write_dataframe_to_sqlite(df, db_name, table_name):
    with sqlite3.connect(db_name) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"DataFrame written to SQLite database '{db_name}' in table '{table_name}'.")

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
    
    if data == 'bio_axv_preprints_microbiology':
        db_name = "collections.sqlite"
        table_name = "preprints"
        with sqlite3.connect(db_name) as conn:
            return pd.read_sql_query(f"SELECT * FROM {table_name} WHERE preprint_category=='microbiology'", conn)
    
    if data == 'bio_axv_embeddings_microbiology':

            # Replace 'your_database.db' with the path to your SQLite database file
            db_path = "collections.sqlite"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Replace 'your_table_name' with the name of the table containing columns a and b
            query = """SELECT embedding 
                        FROM embeddings 
                        INNER JOIN (SELECT published_doi FROM preprints WHERE preprint_category=="microbiology") AS temp
                        ON embeddings.doi = temp.published_doi"""
            cursor.execute(query)

            # Fetch binary data from column b
            binary_data = cursor.fetchall()

            # Close the connection
            conn.close()

            # Convert binary data to NumPy array
            numpy_arrays = [np.frombuffer(row[0], dtype=np.float32) for row in binary_data]
            return np.array(numpy_arrays)

