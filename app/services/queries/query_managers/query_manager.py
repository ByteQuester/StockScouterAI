import sqlite3
import os

class QueryManager:
    def __init__(self, db_path='data.db'):
        self.db_path = os.path.abspath(db_path)  # Ensure the db_path is absolute
        print(f"Database path set to: {self.db_path}")

    def execute_query(self, query_file, params):
        with open(query_file, 'r') as file:
            query = file.read()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Initialize result_dicts to avoid referencing before assignment
        result_dicts = []

        # Split the query into individual statements
        statements = query.strip().split(';')

        # Execute each statement separately
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    print(f"Executing SQL: {statement}")
                    if params and statement.upper().startswith("SELECT"):
                        cursor.execute(statement, params)
                        result = cursor.fetchall()
                        columns = [desc[0] for desc in cursor.description]
                        result_dicts = [dict(zip(columns, row)) for row in result]
                    else:
                        cursor.execute(statement)
                except sqlite3.OperationalError as e:
                    print(f"SQL error: {e}")
                except sqlite3.Error as e:
                    print(f"SQLite error: {e}")

        conn.commit()
        conn.close()

        return result_dicts
