import requests
import sqlite3
from tqdm import tqdm
from utils import (read_dataframe_from_sqlite,
                   write_dataframe_to_sqlite)

print("--------- Scraping bioaxv------------")
def read_last_index():
    try:
        with open('last_index.txt', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def write_last_index(index):
    with open('last_index.txt', 'w') as f:
        f.write(str(index))

# Define the database and create the table
conn = sqlite3.connect('collections.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS preprints
             (preprint_doi TEXT, published_doi TEXT, published_journal TEXT, preprint_platform TEXT, preprint_title TEXT,
              preprint_authors TEXT, preprint_category TEXT, preprint_date TEXT, published_date TEXT,
              preprint_abstract TEXT, preprint_author_corresponding TEXT, preprint_author_corresponding_institution TEXT)''')

# Scrape the data and insert into the database
url_template = "https://api.biorxiv.org/pubs/biorxiv/2020-03-01/2023-03-30/{}"
last_index = read_last_index()

max_n = 66763
for i in tqdm(range(last_index, max_n, 100)):
    url = url_template.format(i)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        break

    data = response.json()

    for entry in data["collection"]:
        c.execute('''INSERT INTO preprints VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            entry.get("preprint_doi", ""),
            entry.get("published_doi", ""),
            entry.get("published_journal", ""),
            entry.get("preprint_platform", ""),
            entry.get("preprint_title", ""),
            entry.get("preprint_authors", ""),
            entry.get("preprint_category", ""),
            entry.get("preprint_date", ""),
            entry.get("published_date", ""),
            entry.get("preprint_abstract", ""),
            entry.get("preprint_author_corresponding", ""),
            entry.get("preprint_author_corresponding_institution", "")
        ))

    conn.commit()
    write_last_index(i)

conn.close()
print("--------- Scraped bioaxv------------")
print("--------- Format database ---------")

df = read_dataframe_from_sqlite("collections.sqlite", "preprints")

# Formatting to make the format compatible with references.py def add_references
df['url'] = 'https://doi.org/'+df['published_doi']

df['citation'] = (df['preprint_title']
                  + ' in '
                  + df['published_journal'] 
                  + ' - Lab: ' 
                  + df['preprint_author_corresponding'] 
                  + ' - Institution: ' 
                  + df['preprint_author_corresponding_institution']
                  )

write_dataframe_to_sqlite(df, 'collections.sqlite', 'preprints')
print("--------- Formatted database ---------")

print("--------- Calculating Abstract Embeddings ------------")
import sqlite3
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def read_dataframe_from_sqlite(db_name, table_name):
    with sqlite3.connect(db_name) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df

df = read_dataframe_from_sqlite("collections.sqlite", "preprints")

def save_embeddings_to_db(con, doi_list, embeddings):
    cur = con.cursor()
    for doi, embedding in zip(doi_list, embeddings):
        array_buffer = embedding.tobytes()
        cur.execute("INSERT OR REPLACE INTO embeddings (doi, embedding) VALUES (?, ?)", (doi, array_buffer))
    con.commit()

def load_embeddings_from_db(con, doi_list):
    cur = con.cursor()
    embeddings = []
    for doi in doi_list:
        cur.execute("SELECT embedding FROM embeddings WHERE doi=?", (doi,))
        row = cur.fetchone()
        if row:
            embedding = np.frombuffer(row[0], dtype=np.float32)
            embeddings.append(embedding)
    return np.array(embeddings)

# Initialize the model
model = SentenceTransformer("allenai/scibert_scivocab_uncased")

# Set up the SQLite database
db_file = "collections.sqlite"
con = sqlite3.connect(db_file)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS embeddings (doi TEXT PRIMARY KEY, embedding BLOB)")

# Define chunk size
chunk_size = 100

# Split DataFrame into chunks and process each chunk
num_chunks = (len(df) - 1) // chunk_size + 1
for i in tqdm(range(num_chunks)):
    chunk = df.iloc[i * chunk_size : (i + 1) * chunk_size]
    abstracts = chunk.preprint_abstract.to_list()
    dois = chunk.published_doi.to_list()

    # Check if embeddings are already in the database
    cached_embeddings = load_embeddings_from_db(con, dois)
    if len(cached_embeddings) == len(dois):
        print(f"Loaded cached embeddings for chunk {i + 1}")
        chunk_embeddings = cached_embeddings
    else:
        print(f"Generating embeddings for chunk {i + 1}")
        chunk_embeddings = model.encode(abstracts)
        save_embeddings_to_db(con, dois, chunk_embeddings)

    # Process chunk_embeddings as needed

# Close the database connection
con.close()
print("--------- Calculated Abstract Embeddings -----------")
print("--------- End of scrape_bioaxv.py script -----------")
