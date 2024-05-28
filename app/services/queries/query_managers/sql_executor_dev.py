# app/services/queries/query_managers/sql_executor.py

import sqlite3


class SQLExecutor:

    def __init__(self, db_path):
        self.db_path = db_path

    def execute_sql_file(self, sql_file):
        with open(sql_file, 'r') as file:
            query = file.read()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.executescript(query)
            conn.commit()
        except Exception as e:
            print(f"Failed to execute {sql_file}: {str(e)}")
        finally:
            conn.close()

    def query_sql(self, sql, params):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(sql, params)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result_dicts = [dict(zip(columns, row)) for row in result]
        except Exception as e:
            print(f"Failed to execute query: {str(e)}")
            result_dicts = []
        finally:
            conn.close()

        return result_dicts
