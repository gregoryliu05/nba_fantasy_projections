import sqlite3
import pandas as pd
import os

db_path = 'database/nba_database.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

csv_directory = 'data/'

def create_table_from_csv(csv_file, conn):
    df = pd.read_csv(csv_file)
    table_name = os.path.splitext(os.path.basename(csv_file))[0]

    df.to_sql(table_name, conn, if_exists='replace', index= False)
    print(f"Table {table_name} created.")

for file_name in os.listdir(csv_directory):
    if file_name.endswith('.csv'):
        csv_file_path = os.path.join(csv_directory, file_name)
        create_table_from_csv(csv_file_path, conn)




