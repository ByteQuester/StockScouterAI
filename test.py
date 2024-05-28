import os
import sqlite3

import pandas as pd

from app.services.queries.query_managers.query_manager import QueryManager

# Ensure the correct working directory
os.chdir('/Users/mpo/Desktop/StockScouterAI-dev-feature-comparatie-analysis')

# Initialize QueryManager with explicit path if needed
query_manager = QueryManager('data.db')

# Define a simplified query directly for the final view
simple_query = """
SELECT * FROM profitability_analysis WHERE CIK = ? AND DATE BETWEEN ? AND ?;
"""

params = ('0000816761', '2020-01-01', '2023-01-01')


# Execute the simplified query and print the result
def execute_simple_query(query, params):
    conn = sqlite3.connect(query_manager.db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    result_dicts = [dict(zip(columns, row)) for row in result]
    conn.close()
    return result_dicts


simple_query_result = execute_simple_query(simple_query, params)
print("Simple query result:", simple_query_result)

# Ensure the query result is a pandas DataFrame
df = pd.DataFrame(simple_query_result)
print("Converted DataFrame:\n", df)
