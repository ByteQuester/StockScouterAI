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

        # Define the tables and their schemas
        tables = {
            "raw_profitability":
            '''
                CREATE TABLE IF NOT EXISTS raw_profitability (
                    ENTITY TEXT,
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
            ''',
            "raw_cash_flow":
            '''
                CREATE TABLE IF NOT EXISTS raw_cash_flow (
                    ENTITY TEXT,
                    CIK TEXT,
                    DATE DATE,
                    Year INTEGER,
                    Quarter TEXT,
                    CASH_FLOW_FINANCING REAL,
                    CASH_FLOW_INVESTING REAL,
                    CASH_FLOW_OPERATING REAL,
                    PRIMARY KEY (CIK, DATE)
                )
            ''',
            "raw_liquidity":
            '''
                CREATE TABLE IF NOT EXISTS raw_liquidity (
                    ENTITY TEXT,
                    CIK TEXT,
                    DATE DATE,
                    Year INTEGER,
                    Quarter TEXT,
                    CURRENT_ASSETS REAL,
                    CURRENT_LIABILITIES REAL,
                    CURRENT_RATIO REAL,
                    PRIMARY KEY (CIK, DATE)
                )
            ''',
            "raw_assets_liabilities":
            '''
                CREATE TABLE IF NOT EXISTS raw_assets_liabilities (
                    ENTITY TEXT,
                    CIK TEXT,
                    DATE DATE,
                    Year INTEGER,
                    Quarter TEXT,
                    ASSETS_CURRENT REAL,
                    LIABILITIES_CURRENT REAL,
                    STOCKHOLDERS_EQUITY REAL,
                    ASSET_TO_LIABILITY_RATIO REAL,
                    DEBT_TO_EQUITY_RATIO REAL,
                    PRIMARY KEY (CIK, DATE)
                )
            '''
        }

        # Create tables
        for table_name, schema in tables.items():
            cursor.execute(schema)

        # Load CSV files into corresponding tables
        for cik in os.listdir(self.base_dir):
            for category in [
                    "Profitability", "Cash_Flow", "Liquidity",
                    "Assets_Liabilities"
            ]:
                folder_path = os.path.join(self.base_dir, cik,
                                           'processed_data', category)
                if os.path.isdir(folder_path):
                    table_name = f'raw_{category.lower()}'
                    for file in os.listdir(folder_path):
                        if file.endswith('.csv'):
                            file_path = os.path.join(folder_path, file)
                            df = pd.read_csv(file_path)
                            df['CIK'] = cik

                            # Remove duplicates
                            existing_dates = pd.read_sql_query(
                                f"SELECT DATE FROM {table_name} WHERE CIK='{cik}'",
                                conn)
                            existing_dates = existing_dates['DATE'].tolist()
                            df = df[~df['DATE'].isin(existing_dates)]

                            if not df.empty:
                                df.to_sql(table_name,
                                          conn,
                                          if_exists='append',
                                          index=False)
                                print(
                                    f"Loaded data from {file_path} into {table_name}"
                                )
                            else:
                                print(f"No new data to load from {file_path}")

        conn.commit()
        conn.close()
