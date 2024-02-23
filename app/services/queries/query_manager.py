import pandas as pd

from app.services.functions.managers import LoggingManager

from .base_tables import ASSET_LIABILITIES, CASH_FLOW, LIQUIDITY, PROFITABILITY
from .sql_tables import SQL_QUERY_FILES


class QueryExecutor:
    """
    Args:
            snowflake_manager: Snowflake manager for executing queries in Snowflake.
            data_storage_manager: Data storage manager for executing queries locally.
    """

    def __init__(self, snowflake_manager, data_storage_manager):
        self.snowflake_manager = snowflake_manager
        self.data_storage_manager = data_storage_manager
        self.error_handler = LoggingManager()

    def execute_query(self, query_names, use_snowflake) -> dict:
        """
        Executes one or more queries, either locally or in Snowflake.

        Args:
            query_names (str or list of str): Name or names of the queries to execute.
            use_snowflake (bool): Flag indicating whether to execute queries in Snowflake.

        Returns:
            dict: A dictionary where keys are query names, and values are query results.

        This method allows you to execute one or more queries, either locally or in Snowflake, based on the provided
        `query_names` and `use_snowflake` flag.

        Raises:
            ValueError: If `query_names` is not a valid query name or a list of valid query names.

        Example:
            >>> query_names = 'Assets Liabilities'
            >>> use_snowflake = True
            >>> results = QueryExecutor.execute_query(query_names, use_snowflake)
        """
        if isinstance(query_names, str):
            query_names = [query_names]

        results = {}
        for query_name in query_names:
            if use_snowflake:
                results[query_name] = self._execute_query_snowflake(query_name)
            else:
                results[query_name] = self._execute_query_locally(query_name)

        return results

    def _execute_query_snowflake(self, query_name) -> pd.DataFrame:
        """
        Executes a query in Snowflake.

        Args:
            query_name (str): Name of the query.

        Returns:
            pd.DataFrame: Result of the query as a DataFrame.

        Raises:
            ValueError: If the provided `query_name` is not found.
        """
        query_filename = SQL_QUERY_FILES.get(query_name)
        if query_filename:
            return self.snowflake_manager.execute_query_from_file(
                query_filename)
        else:
            self.error_handler.log(f"Query name '{query_name}' not found.",
                                   "ERROR")
            return None

    def _execute_query_locally(self, query_name) -> pd.DataFrame:
        """
        Executes a query locally.

        Args:
            query_name (str): Name of the query.

        Returns:
            pd.DataFrame: Result of the query as a DataFrame.

        Raises:
            ValueError: If no processed data file is found for the query.
        """
        file_path = self.data_storage_manager.get_latest_file_path(
            query_name, 'preprocessed_data')
        if not file_path:
            self.error_handler.log(
                f"No processed data file found for query {query_name}.",
                "ERROR")
            return None
        df = pd.read_csv(file_path)

        return self._run_local_query(df, query_name)

    def _run_local_query(self, df, query_name) -> pd.DataFrame:
        """
        Runs a local query based on the query name.

        Args:
            df (pd.DataFrame): DataFrame containing the data.
            query_name (str): Name of the query.

        Returns:
            pd.DataFrame: Result of the query as a DataFrame.

        Raises:
            ValueError: If the provided `query_name` is not implemented for local execution.
        """
        query_classes = {
            'Assets Liabilities': ASSET_LIABILITIES,
            'Cash Flow': CASH_FLOW,
            'Liquidity': LIQUIDITY,
            'Profitability': PROFITABILITY
        }
        if query_name in query_classes:
            query_class = query_classes[query_name]()
            return query_class.run_query(df)
        else:
            self.error_handler.log(
                f"Query name '{query_name}' not implemented for local execution.",
                "ERROR")
            return None
