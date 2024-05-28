import sqlite3


class ViewManager:

    def __init__(self, db_path='data.db'):
        self.db_path = db_path

    def execute_sql_file(self, sql_file):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            with open(sql_file, 'r') as file:
                query = file.read()
            cursor.executescript(query)
            conn.commit()
        except Exception as e:
            print(f"Failed to execute {sql_file}: {str(e)}")
        finally:
            conn.close()
