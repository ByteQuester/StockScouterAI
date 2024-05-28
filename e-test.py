import os
import sqlite3

import pandas as pd

from app.services.queries.query_managers.query_manager import QueryManager

# Set the current working directory to your project root if necessary
os.chdir('/Users/mpo/Desktop/StockScouterAI-dev-feature-comparatie-analysis')

# Initialize QueryManager with explicit path if needed
query_manager = QueryManager('data.db')

# Define the query file and parameters
query_file = 'app/services/queries/sql_views/NULL_profitability_views.sql'
params = ('0000816761', '2020-01-01', '2023-01-01')


def load_query(query_file):
    with open(query_file, "r") as f:
        return f.read()


# Load and print the query
query = load_query(query_file)
print("SQL query content:\n", query)

# Execute the query and print the result
query_result = query_manager.execute_query(query_file, params)
print("Query result:", query_result)

# Ensure the query result is a pandas DataFrame
df = pd.DataFrame(query_result)
print("Converted DataFrame:\n", df)
