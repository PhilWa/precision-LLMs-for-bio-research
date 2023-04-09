import sqlite3
import pandas as pd
import pytest

DATABASE_PATH = "collections.sqlite"
TABLES = [
    {
        "name": "pathbank_all_metabolites",
        "primary_key": ["PathBank_ID", "Metabolite_ID"],
    },
    # {"name": "pathbank_all_proteins", "primary_key": ["PathBank_ID", "Uniprot_ID"]},
    {"name": "pathbank_pathways", "primary_key": ["SMPDB_ID"]},
]


def connect_to_db(database_path):
    conn = sqlite3.connect(database_path)
    return conn


@pytest.fixture(scope="module")
def connection():
    conn = connect_to_db(DATABASE_PATH)
    yield conn
    conn.close()


@pytest.mark.parametrize("table", TABLES)
def test_primary_key_violations(connection, table):
    table_name = table["name"]
    primary_key_columns = table["primary_key"]
    primary_key_columns_str = ", ".join(primary_key_columns)

    # Check for duplicate primary keys
    group_by_columns = ", ".join(primary_key_columns)
    query = f"SELECT COUNT(*) as count, {primary_key_columns_str} FROM {table_name} GROUP BY {group_by_columns} HAVING count > 1;"
    duplicates = pd.read_sql_query(query, connection)
    print(duplicates)

    assert (
        len(duplicates) == 0
    ), f"Found {len(duplicates)} duplicate primary keys in {table_name}."

    # Check for missing primary keys
    missing_conditions = " OR ".join([f"{col} IS NULL" for col in primary_key_columns])
    query = f"SELECT * FROM {table_name} WHERE {missing_conditions};"
    missing_pks = pd.read_sql_query(query, connection)
    if len(missing_pks) > 0:
        print(f"Rows with missing primary keys in {table_name}:")
        print(missing_pks)
    assert (
        len(missing_pks) == 0
    ), f"Found {len(missing_pks)} rows with missing primary keys in {table_name}."


if __name__ == "__main__":
    pytest.main([__file__])
