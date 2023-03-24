from sentence_transformers import SentenceTransformer
import pandas as pd

if False:
    model = SentenceTransformer("all-mpnet-base-v2")

    abstracts = pd.read_excel("data/abstracts/Book1.xlsx")
    abstract_embedding = model.encode(abstracts.abstract.to_list())
    pd.DataFrame(abstract_embedding).to_csv("data/abstracts/abstract_embeddings.csv")


import os
import json
import pandas as pd
import sqlite3

def load_collection_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['collection']

def load_collections_from_directory(directory):
    json_files = [file for file in os.listdir(directory) if file.endswith('.json')]

    collections = []
    for json_file in json_files:
        file_path = os.path.join(directory, json_file)
        collection = load_collection_from_json(file_path)
        collections.extend(collection)

    return pd.DataFrame(collections)

def write_dataframe_to_sqlite(df, db_name, table_name):
    with sqlite3.connect(db_name) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"DataFrame written to SQLite database '{db_name}' in table '{table_name}'.")

if __name__ == "__main__":
    directory = "data/abstracts/json"
    df = load_collections_from_directory(directory)

    db_name = "collections.sqlite"
    table_name = "collection_data"
    write_dataframe_to_sqlite(df, db_name, table_name)


import os
import json
import pandas as pd
import sqlite3

db_name = "collections.sqlite"
table_name = "collection_data"

def read_dataframe_from_sqlite(db_name, table_name):
    with sqlite3.connect(db_name) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df

df = read_dataframe_from_sqlite("collections.sqlite", "collection_data")

df = (df.sort_values(['doi', 'version'], ascending=[True, False])
               .drop_duplicates(subset='doi', keep='first')
               .reset_index(drop=True)
            )

# Formatting to make the format compatible with references.py def add_references
df['url'] = 'https://doi.org/'+df['doi']

df['citation'] = (df['title'] 
                  + ' - Lead: ' 
                  + df['author_corresponding'] 
                  + ' - Institution: ' 
                  + df['author_corresponding_institution']
                  )

import pandas as pd
import sqlite3

def write_dataframe_to_sqlite(df, db_name, table_name):
    with sqlite3.connect(db_name) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"DataFrame written to SQLite database '{db_name}' in table '{table_name}'.")

write_dataframe_to_sqlite(df, db_name='collections.sqlite', table_name='bioarchive_abstracts')