import pandas as pd

from ..pre_processing import AnnualDataProcessor, QuarterlyDataProcessor


class DataPreprocessor:
    """
    Handles preprocessing of raw data fetched from the SEC API.

    This class manages the preprocessing of data based on defined metrics and
    stores or uploads the processed data using the appropriate storage manager.

    Attributes:
        data_storage_manager (DataStorageManager): Manages local data storage operations.
        file_version_manager (FileVersionManager): Manages file versioning and indexing.
        error_handler (LoggingManager): Handles logging of errors and informational messages.
        snowflake_manager (SnowflakeDataManager, optional): Manages data upload to Snowflake. Default is None.
    """

    def __init__(self,
                 data_storage_manager,
                 file_version_manager,
                 error_handler,
                 snowflake_manager=None):
        """
        Initializes the DataPreprocessor with necessary managers and handlers.

        Args:
            data_storage_manager (DataStorageManager): Manages local data storage operations.
            file_version_manager (FileVersionManager): Manages file versioning and indexing.
            error_handler (LoggingManager): Handles logging of errors and informational messages.
            snowflake_manager (SnowflakeDataManager, optional): Manages data upload to Snowflake. Default is None.
        """
        self.data_storage_manager = (data_storage_manager)
        self.file_version_manager = (file_version_manager)
        self.error_handler = (error_handler)
        self.snowflake_manager = (snowflake_manager)

    def preprocess_data(self, raw_data: dict, category_metric_map: dict,
                        use_snowflake: bool, cik_number: str) -> dict:
        """
        Preprocesses the raw data using annual and quarterly data processors.

        Args:
            raw_data (dict): The raw data fetched from the SEC API.
            category_metric_map (dict): A mapping of data categories to their respective metrics.
            use_snowflake (bool): Flag to indicate whether to upload data to Snowflake.
            cik_number (str): Central Index Key number for data categorization.

        Returns:
            dict: Processed data or an error message.
        """
        try:
            df = pd.DataFrame(raw_data)
            annual_processor = AnnualDataProcessor(df)
            quarterly_processor = QuarterlyDataProcessor(df)

            for category, metrics in category_metric_map.items():
                preprocessed_data = self._process_data(category, metrics,
                                                       annual_processor,
                                                       quarterly_processor)
                self._store_or_upload_data(preprocessed_data, category,
                                           use_snowflake, cik_number)

        except Exception as e:
            self.error_handler.log_error(e, "ERROR")
            return {"error": str(e)}

    def _process_data(
            self, category: str, metrics: list,
            annual_processor: AnnualDataProcessor,
            quarterly_processor: QuarterlyDataProcessor) -> pd.DataFrame:
        """
        Processes data for a given category using the appropriate processor.

        Args:
            category (str): The category of data to be processed.
            metrics (list): List of metrics associated with the category.
            annual_processor (AnnualDataProcessor): Processor for annual data.
            quarterly_processor (QuarterlyDataProcessor): Processor for quarterly data.

        Returns:
            DataFrame: Processed data for the given category.
        """
        if category in ['Assets Liabilities', 'Liquidity', 'Profitability']:
            return quarterly_processor.process_data(metrics)
        else:
            return annual_processor.process_data(metrics)

    def _store_or_upload_data(self, preprocessed_data: pd.DataFrame,
                              category: str, use_snowflake: bool,
                              cik_number: str):
        """
        Stores or uploads the preprocessed data based on the storage type.

        Args:
            preprocessed_data (DataFrame): The preprocessed data to be stored or uploaded.
            category (str): The category of data being processed.
            use_snowflake (bool): Flag to indicate whether to upload data to Snowflake.
            cik_number (str): Central Index Key number for data categorization.
        """
        if use_snowflake and self.snowflake_manager:
            self.snowflake_manager.upload_data(preprocessed_data, category)
            self.error_handler.log(
                f"Preprocessed data for {category} uploaded to Snowflake.",
                "INFO")
        else:
            file_name = self.data_storage_manager.store_data(
                preprocessed_data, 'preprocessed_data', category)
            if file_name:
                self.file_version_manager.update_index(cik_number, category,
                                                       file_name,
                                                       'preprocessed_data')
            else:
                self.error_handler.log(
                    f"Failed to store preprocessed data for {category}",
                    "ERROR")
