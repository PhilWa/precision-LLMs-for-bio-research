from utils import write_dataframe_to_sqlite
import pandas as pd


df = pd.read_csv('data/pathbank_all_metabolites.csv')
DB_NAME = 'pathbank_all_metabolites'
TABLE_NAME = 'pathbank_all_metabolites'
write_dataframe_to_sqlite(df, DB_NAME, TABLE_NAME)
del df
print('------ Done ------')