# data_loader.py

import os
import sqlite3

import pandas as pd


class DataLoader:

    def __init__(self, base_dir='data', db_path='data.db'):
        self.base_dir = base_dir
        self.db_path = db_path

    def load_data_to_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create raw data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS raw_profitability (
                EntityName TEXT,
                CIK TEXT,
                DATE DATE,
                Year INTEGER,
                Quarter TEXT,
                NET_INCOME_LOSS REAL,
                OPS_INCOME_LOSS REAL,
                REVENUES REAL,
                PROFIT_MARGIN REAL,
                PRIMARY KEY (CIK, DATE)
            )
        ''')

        for cik in os.listdir(self.base_dir):
            folder_path = os.path.join(self.base_dir, cik, 'processed_data',
                                       'Profitability')
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith('.csv'):
                        file_path = os.path.join(folder_path, file)
                        df = pd.read_csv(file_path)
                        df['CIK'] = cik
                        df.to_sql('raw_profitability',
                                  conn,
                                  if_exists='append',
                                  index=False)
        conn.commit()
        conn.close()
