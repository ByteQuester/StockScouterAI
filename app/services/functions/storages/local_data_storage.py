import json
import os
from typing import Optional, Union

import pandas as pd

from app.services.functions.managers import LoggingManager
from app.services.types import QueryFolderMapping
from app.services.utils import now


class DataStorageManager:

    def __init__(self, local_storage_dir: str, cik_number: str):
        """
        Initialize the DataStorageManager.

        Args:
            local_storage_dir (str): The base directory for local storage.
            cik_number (str): The Central Index Key number.
        """
        self.local_storage_dir = local_storage_dir
        self.cik_number = cik_number
        self.error_handler = LoggingManager()

    def _generate_file_name(self,
                            category_name: Optional[str],
                            timestamp: str,
                            extension: str,
                            sub_category: Optional[str] = None) -> str:
        """
        Generate a file name based on category, sub-category, and timestamp.

        Args:
            category_name (str): The name of the category.
            timestamp (str): The timestamp to include in the file name.
            extension (str): The file extension (e.g., 'csv', 'json').
            sub_category (str, optional): The sub-category name. Defaults to None.

        Returns:
            str: The generated file name.
        """
        parts = [self.cik_number]
        if category_name:
            parts.append(category_name.replace(' ', '_'))
        if sub_category:
            parts.append(sub_category.replace(' ', '_'))
        parts.append(timestamp)
        return f"{'_'.join(parts)}.{extension}"

    def _create_directory_path(self,
                               storage_type: str,
                               category_name: str = None,
                               sub_category: str = None) -> str:
        """
        Create a directory path based on storage type, category, and sub-category.

        Args:
            storage_type (str): The storage type ('preprocessed_data' or 'processed_data').
            category_name (str, optional): The category name. Default is None.
            sub_category (str, optional): The sub-category name. Default is None.

        Returns:
            str: The generated directory path.
        """
        dir_parts = [
            self.local_storage_dir,
            str(self.cik_number), storage_type
        ]
        if category_name:
            dir_parts.append(category_name.replace(' ', '_'))
        if sub_category:
            dir_parts.append(sub_category.replace(' ', '_'))
        dir_path = os.path.join(*dir_parts)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path

    def store_data(self,
                   data: pd.DataFrame,
                   storage_type: str,
                   category_name: str = None) -> Union[str, None]:
        """
        Store data in CSV format.

        Args:
            data (pd.DataFrame): The data to be stored as a DataFrame.
            storage_type (str): The storage type ('preprocessed_data' or 'processed_data').
            category_name (str, optional): The category name. Default is None.

        Returns:
            Union[str, None]: The file name of the stored data or None if an error occurs.
        """
        timestamp = now()
        dir_path = self._create_directory_path(storage_type, category_name)
        file_name = self._generate_file_name(category_name, timestamp, 'csv')
        file_path = os.path.join(dir_path, file_name)
        data.to_csv(file_path, index=False)
        self.error_handler.log(f"Data stored locally at {file_path}", "INFO")
        return file_name

    def store_json_data(self,
                        json_data: dict,
                        storage_type: str,
                        category_name: str = None,
                        sub_category: str = None) -> Union[str, None]:
        """
        Store JSON data in the designated directory for specific chart types.

        Args:
            json_data (dict): The JSON data to be stored.
            storage_type (str): The storage type ('preprocessed_data' or 'processed_data').
            category_name (str, optional): The category name. Default is None.
            sub_category (str, optional): The sub-category name. Default is None.

        Returns:
            Union[str, None]: The file name of the stored JSON data or None if an error occurs.
        """
        timestamp = now()
        dir_path = self._create_directory_path(storage_type, category_name,
                                               sub_category)
        file_name = self._generate_file_name(category_name, timestamp, 'json',
                                             sub_category)
        file_path = os.path.join(dir_path, file_name)
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        self.error_handler.log(f"JSON data stored locally at {file_path}",
                               "INFO")
        return file_name

    def get_latest_file_path(self, query_name: str,
                             data_type: str) -> Union[str, None]:
        """
        Get the path of the latest file for a specific query in a specified data type directory.
        Args:
            query_name (str): The name of the query.
            data_type (str): Type of data ('preprocessed_data' or 'processed_data').
        Returns:
            Union[str, None]: The path of the latest file, or None if no file is found.
        """
        dir_path = self._get_directory_path(query_name, data_type)
        if dir_path is None:
            return None

        try:
            files = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
            if not files:
                self.error_handler.log(
                    f"No files found for query {query_name}.", "WARNING")
                return None

            latest_file = max(files, key=os.path.getmtime)
            return latest_file
        except Exception as e:
            self.error_handler.log_error(e, "ERROR")
            return None

    def _get_directory_path(self, query_name: str,
                            data_type: str) -> Union[str, None]:
        folder_name = QueryFolderMapping.get_folder_name(query_name)
        if not folder_name:
            self.error_handler.log(
                f"No folder mapping found for query {query_name}.", "ERROR")
            return None

        dir_path = os.path.join(self.local_storage_dir, str(self.cik_number),
                                data_type, folder_name)
        if not os.path.isdir(dir_path):
            self.error_handler.log(
                f"Directory not found for query {query_name}.", "ERROR")
            return None

        return dir_path
