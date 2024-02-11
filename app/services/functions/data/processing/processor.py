class DataProcessor:
    """
    Manages the processing and storage of preprocessed data.

    This class takes care of running specific queries on preprocessed data, handling the results,
    and ensuring that they are appropriately stored or logged.

    Attributes:
        data_storage_manager (DataStorageManager): Manages local data storage operations.
        file_version_manager (FileVersionManager): Manages file versioning and indexing.
        query_executor (QueryExecutor): Executes data processing queries.
        error_handler (LoggingManager): Handles logging of errors and informational messages.
    """

    def __init__(self, data_storage_manager, file_version_manager,
                 query_executor, error_handler):
        """
        Initializes the DataProcessor with necessary managers and handlers.

        Args:
            data_storage_manager (DataStorageManager): Manages local data storage operations.
            file_version_manager (FileVersionManager): Manages file versioning and indexing.
            query_executor (QueryExecutor): Executes data processing queries.
            error_handler (LoggingManager): Handles logging of errors and informational messages.
        """
        self.data_storage_manager = (data_storage_manager)
        self.file_version_manager = (file_version_manager)
        self.query_executor = (query_executor)
        self.error_handler = (error_handler)

    def process_and_store_data(self,
                               category_metric_map: dict,
                               use_snowflake: bool,
                               cik_number: str,
                               specific_queries: list = None) -> dict:
        """
        Processes and stores data based on specific queries or all available categories.

        Args:
            category_metric_map (dict): A mapping of data categories to their respective metrics.
            use_snowflake (bool): Flag to indicate whether to upload data to Snowflake.
            cik_number (str): Central Index Key number for data categorization.
            specific_queries (list of str, optional): Specific queries to execute. Default is None.

        Returns:
            dict: Processed data or an error message.
        """
        try:
            categories_to_process = specific_queries if specific_queries else category_metric_map.keys(
            )

            for category in categories_to_process:
                if category not in category_metric_map:
                    self.error_handler.log(
                        f"Invalid category or query name: {category}",
                        "WARNING")
                    continue

                preprocessed_file_path = self.data_storage_manager.get_latest_file_path(
                    category, 'preprocessed_data')
                if not preprocessed_file_path:
                    self.error_handler.log(
                        f"No preprocessed data found for {category}",
                        "WARNING")
                    continue

                query_result = self.query_executor.execute_query(
                    category, use_snowflake)
                self._store_and_log_data(query_result, category, cik_number)

        except Exception as e:
            self.error_handler.log_error(e, "ERROR")
            return {"error": str(e)}

    def _store_and_log_data(self, query_result: dict, category: str,
                            cik_number: str) -> None:
        """
        Stores the query results in the appropriate format and logs any errors or warnings.

        Args:
            query_result (dict): The result of the executed query.
            category (str): The category of the processed data.
            cik_number (str): Central Index Key number for data categorization.
        """
        if query_result and category in query_result and query_result[
                category] is not None:
            processed_file_name = self.data_storage_manager.store_data(
                query_result[category], 'processed_data', category)
            if processed_file_name:
                self.file_version_manager.update_index(cik_number, category,
                                                       processed_file_name,
                                                       'processed_data')
            else:
                self.error_handler.log(
                    f"Failed to store processed data for {category}", "ERROR")
        else:
            self.error_handler.log(f"No valid results for query {category}.",
                                   "WARNING")
