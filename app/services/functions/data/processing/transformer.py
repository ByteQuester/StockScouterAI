from typing import Dict, List, Optional

import pandas as pd


class JSONDataTransformer:
    """
    Manages the transformation of processed data into JSON format and its storage.

    This class handles the conversion of data into a JSON format suitable for charts or other visualizations,
    and ensures that this transformed data is stored correctly.

    Attributes:
        data_storage_manager (DataStorageManager): Manages local data storage operations.
        transformer_manager (TransformerManager): Manages data transformation operations.
        error_handler (LoggingManager): Handles logging of errors and informational messages.
    """

    def __init__(self, data_storage_manager, transformer_manager,
                 error_handler) -> None:
        self.data_storage_manager = data_storage_manager
        self.transformer_manager = transformer_manager
        self.error_handler = error_handler

    def transform_and_store(self,
                            category_metric_map: Dict[str, List[str]],
                            specific_category: Optional[str] = None,
                            chart_types: Optional[List[str]] = None) -> None:
        """
        Transforms and stores data in JSON format based on the specified categories and chart types.

        Args:
            category_metric_map (Dict[str, List[str]]): A mapping of data categories to their respective metrics.
            specific_category (Optional[str]): Specific category to process. Default is None.
            chart_types (Optional[List[str]]): Specific chart types to transform data into. Default is None.

        Returns:
            None
        """
        categories_to_process = [
            specific_category
        ] if specific_category else category_metric_map.keys()

        for category in categories_to_process:
            processed_file_path = self.data_storage_manager.get_latest_file_path(
                category, 'processed_data')
            if not processed_file_path:
                self.error_handler.log(
                    f"No processed data found for {category}", "WARNING")
                continue

            df = pd.read_csv(processed_file_path)
            transformed_json = self._transform_data(df, category, chart_types)
            self._store_json_data(transformed_json, category)

    def _transform_data(self, df: pd.DataFrame, category: str,
                        chart_types: Optional[List[str]]) -> Dict[str, dict]:
        """
        Transforms data into JSON format for a given category and chart types.

        Args:
            df (pd.DataFrame): The DataFrame containing processed data.
            category (str): The category of the processed data.
            chart_types (Optional[List[str]]): List of specific chart types to transform data into.

        Returns:
            Dict[str, dict]: Transformed data in JSON format for each chart type.
        """
        if chart_types is None:
            transformed_json = self.transformer_manager.transform_data(
                df, category, None)
            return transformed_json
        else:
            transformed_data = {}
            for chart_type in chart_types:
                transformed_data[
                    chart_type] = self.transformer_manager.transform_data(
                        df, category, chart_type)
            return transformed_data

    def _store_json_data(self, transformed_json: Dict[str, dict],
                         category: str) -> None:
        """
        Stores the transformed JSON data.

        Args:
            transformed_json (Dict[str, dict]): Transformed data in JSON format.
            category (str): The category of the processed data.

        Returns:
            None
        """
        for chart_type, data in transformed_json.items():
            sub_category = chart_type if chart_type else "general"
            json_file_name = self.data_storage_manager.store_json_data(
                data, 'processed_json', category, sub_category)
            if not json_file_name:
                self.error_handler.log(
                    f"Failed to store transformed JSON for {category} - {sub_category}",
                    "ERROR")
