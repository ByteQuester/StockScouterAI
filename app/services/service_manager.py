from .configs import SnowflakeConfig
from .functions import (DataPreprocessor, DataProcessor, DataStorageManager,
                        JSONDataTransformer, LoggingManager, SECAPIClient,
                        SnowflakeDataManager, TransformerManager)
from .queries import QueryExecutor
from .types import (ANNUAL_METRICS, ASSET_LIABILITIES_METRICS,
                    CASH_FLOW_METRICS, LIQUIDITY_METRICS,
                    PROFITABILITY_METRICS, QUARTERLY_METRICS)
from .utils import FileVersionManager


class SECDataFetcher:
    """
    Class for handling SEC data fetching.

    Attributes:
        sec_client (SECAPIClient): The SEC API client for data retrieval.

    Methods:
        fetch_company_data(cik_number): Fetch data for a company using its CIK number.

    Example:
        >>> sec_client = SECAPIClient()
        >>> data_fetcher = SECDataFetcher(sec_client)
        >>> company_data = data_fetcher.fetch_company_data('0000012927')
        >>> print(company_data)
    """

    def __init__(self, sec_client: SECAPIClient):
        self.sec_client = sec_client

    def fetch_company_data(self, cik_number: str) -> dict:
        """
        Fetch data for a company using its CIK number.

        Args:
            cik_number (str): The Central Index Key (CIK) of the company.

        Returns:
            dict: The fetched data or an error message.

        Example:
            >>> sec_client = SECAPIClient()
            >>> data_fetcher = SECDataFetcher(sec_client)
            >>> company_data = data_fetcher.fetch_company_data('0000012927')
            >>> print(company_data)
        """
        try:
            company_facts = self.sec_client.fetch_company_facts(cik_number)
            if 'error' in company_facts:
                return {
                    'error':
                    f"Error fetching data for CIK {cik_number}: {company_facts['error']}"
                }
            return company_facts
        except Exception as e:
            return {'error': str(e)}


class DataPipelineIntegration:
    """
    Integrates various data processing stages for SEC data, including fetching, preprocessing, processing,
    and transforming into JSON format.

    Attributes:
        cik_number (str): Central Index Key (CIK) number for querying SEC data.
        use_snowflake (bool): Flag to determine if Snowflake database is used for storage.

    Methods:
        fetch_data: Fetches data from the SEC API using a CIK number.
        preprocess_data: Preprocesses raw data fetched from the SEC API.
        process_and_store_data: Processes preprocessed data and stores or uploads results.
        transform_and_store_json: Transforms data into JSON format and stores it.

    Example:
        >>> cik_number = '0000012927'
        >>> use_snowflake = False
        >>> data_pipeline = DataPipelineIntegration(cik_number, use_snowflake)
        >>> raw_data = data_pipeline.fetch_data()
        >>> preprocessed_data = data_pipeline.preprocess_data(raw_data)
        >>> processed_data = data_pipeline.process_and_store_data()
        >>> json_data = data_pipeline.transform_and_store_json()
    """

    def __init__(self,
                 cik_number: str = None,
                 use_snowflake: bool = True,
                 snowflake_config: SnowflakeConfig = None,
                 local_storage_dir: str = 'data'):
        """
        Initializes the DataPipelineIntegration with necessary configurations and clients.

        Args:
            cik_number (str): Central Index Key (CIK) number of a company.
            use_snowflake (bool): Flag to indicate whether to use Snowflake for storage.
            snowflake_config (SnowflakeConfig): Configuration for Snowflake connection.
            local_storage_dir (str): Directory path for local data storage.
        Other attributes:
            data_storage_manager (DataStorageManager): Manages data storage operations.
            document (FileVersionManager): Manages file versioning and indexing.
            error_handler (LoggingManager): Handles logging of errors and information.
            sec_client (SECAPIClient): Client for fetching data from SEC API.
            transformer_manager (TransformerManager): Manages data transformation processes.
            sec_data_fetcher (SECDataFetcher): Fetches data from the SEC API.
            query_executor (QueryExecutor): Executes queries on the data.
            data_preprocessor (DataPreprocessor): Processes raw SEC data.
            data_processor (DataProcessor): Processes preprocessed data and stores results.
            json_data_transformer (JSONDataTransformer): Transforms and stores data in JSON format.
        """
        # Initialization
        self.cik_number = cik_number
        self.data_storage_manager = DataStorageManager(local_storage_dir,
                                                       cik_number)
        self.document = FileVersionManager(base_dir=local_storage_dir)
        self.error_handler = LoggingManager()
        self.sec_client = SECAPIClient()
        self.sec_data_fetcher = SECDataFetcher(self.sec_client)
        self.transformer_manager = TransformerManager()

        # Initialize processor attributes
        self.data_preprocessor = None
        self.data_processor = None
        self.json_data_transformer = None

        # Metrics initialization
        self._init_metrics()

        # Snowflake related initialization
        self.use_snowflake = use_snowflake
        if self.use_snowflake:
            self.snowflake_config = snowflake_config if snowflake_config else SnowflakeConfig(
            )
            self.snowflake_manager = SnowflakeDataManager(
                self.snowflake_config)
        self.query_executor = QueryExecutor(
            self.snowflake_manager if self.use_snowflake else None,
            self.data_storage_manager)

    def _init_metrics(self):
        self.metrics = {
            'Annual': ANNUAL_METRICS,
            'Quarterly': QUARTERLY_METRICS
        }
        self.category_metric_map = {
            'Assets Liabilities': ASSET_LIABILITIES_METRICS,
            'Cash Flow': CASH_FLOW_METRICS,
            'Liquidity': LIQUIDITY_METRICS,
            'Profitability': PROFITABILITY_METRICS,
        }

    def fetch_data(self, cik_number=None):
        """
        Fetches data from the SEC API using the given CIK number.

        Args:
            cik_number (str, optional): CIK number to fetch data for. If None, uses the CIK number provided during
            initialization.

        Returns:
            dict: Fetched data or error information.
        """
        cik = cik_number if cik_number else self.cik_number
        if not cik:
            self.error_handler.log("CIK number is not provided.", "ERROR")
            return {"error": "CIK number is required"}
        return self.sec_data_fetcher.fetch_company_data(cik)

    def preprocess_data(self, raw_data: dict) -> dict:
        """
        Preprocesses raw data fetched from the SEC API.

        Args:
            raw_data (dict): Raw data fetched from the SEC API.

        Returns:
            dict: Preprocessed data or error information.

        Example:
            >>> cik_number = '0000012927'
            >>> data_pipeline = DataPipelineIntegration(cik_number='0000012927', use_snowflake=False)
            >>> raw_data = data_pipeline.fetch_data()
            >>> preprocessed_data = data_pipeline.preprocess_data(raw_data)
            >>> print(preprocessed_data)
        """
        self.data_preprocessor = DataPreprocessor(
            self.data_storage_manager, self.document, self.error_handler,
            self.snowflake_manager if self.use_snowflake else None)
        return self.data_preprocessor.preprocess_data(raw_data,
                                                      self.category_metric_map,
                                                      self.use_snowflake,
                                                      self.cik_number)

    def process_and_store_data(self, specific_queries: dict = None) -> dict:
        """
        Processes preprocessed data and stores or uploads results.

        Args:
            specific_queries (dict, optional): Specific queries to process.

        Returns:
            dict: Processed and stored data or error information.

        Example:
            >>> cik_number = '0000012927'
            >>> specific_queries = 'Assets Liabilities'
            >>> data_pipeline = DataPipelineIntegration(cik_number, use_snowflake=False)
            >>> raw_data = data_pipeline.fetch_data()
            >>> preprocessed_data = data_pipeline.preprocess_data(raw_data)
            >>> processed_data = data_pipeline.process_and_store_data()
            >>> print(processed_data)
        """
        self.data_processor = DataProcessor(self.data_storage_manager,
                                            self.document, self.query_executor,
                                            self.error_handler)
        return self.data_processor.process_and_store_data(
            self.category_metric_map, self.use_snowflake, self.cik_number,
            specific_queries)

    def transform_and_store_json(self,
                                 specific_category: str = None,
                                 chart_types: list = None) -> dict:
        """
        Transforms data into JSON format and stores it.

        Args:
            specific_category (str, optional): Specific data category to transform.
            chart_types (list, optional): List of chart types to transform.

        Returns:
            dict: Transformed and stored data in JSON format or error information.

        Example:
            >>> cik_number = '0000012927'
            >>> specific_queries = 'Assets Liabilities'
            >>> data_pipeline = DataPipelineIntegration(cik_number, use_snowflake=False)
            >>> raw_data = data_pipeline.fetch_data()
            >>> preprocessed_data = data_pipeline.preprocess_data(raw_data)
            >>> processed_data = data_pipeline.process_and_store_data()
            >>> json_data = data_pipeline.transform_and_store_json()
            >>> print(processed_data)
        """
        self.json_data_transformer = JSONDataTransformer(
            self.data_storage_manager, self.transformer_manager,
            self.error_handler)
        self.json_data_transformer.transform_and_store(
            self.category_metric_map, specific_category, chart_types)
