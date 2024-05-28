import sqlite3


class SQLExecutor:

    def __init__(self, db_path='data.db'):
        self.db_path = db_path

    def execute_sql(self, sql):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            print(f"Executing SQL:\n{sql}")
            cursor.executescript(sql)
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQL error: {e}")
        finally:
            conn.close()

    def query_sql(self, sql, params=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            print(f"Executing Query:\n{sql}")
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result_dicts = [dict(zip(columns, row)) for row in result]
            return result_dicts
        except sqlite3.Error as e:
            print(f"SQL error: {e}")
            return []
        finally:
            conn.close()
