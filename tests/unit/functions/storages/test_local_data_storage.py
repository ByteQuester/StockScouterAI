import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from app.services.functions import DataStorageManager, LoggingManager
from app.services.types import QueryFolderMapping


class TestDataStorageManager(unittest.TestCase):
    def setUp(self):
        self.local_storage_dir = "/tmp/test_storage"
        self.cik_number = "1234567890"
        self.manager = DataStorageManager(self.local_storage_dir, self.cik_number)

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_create_directory_path(self, mock_exists, mock_makedirs):
        storage_type = "preprocessed_data"
        category_name = "test_category"
        expected_dir = f"{self.local_storage_dir}/{self.cik_number}/{storage_type}/{category_name}".replace(' ', '_')
        dir_path = self.manager._create_directory_path(storage_type, category_name)
        mock_makedirs.assert_called_once_with(expected_dir)
        self.assertEqual(dir_path, expected_dir)

    @patch('os.path.join', side_effect=lambda *args: "/".join(args))
    def test_generate_file_name(self, mock_join):
        category_name = "test_category"
        timestamp = "20240101_120000"
        extension = "csv"
        expected_file_name = f"{self.cik_number}_{category_name.replace(' ', '_')}_{timestamp}.{extension}"
        file_name = self.manager._generate_file_name(category_name, timestamp, extension)
        self.assertEqual(file_name, expected_file_name)

    @patch('pandas.DataFrame.to_csv')
    @patch('app.services.functions.storages.local_data_storage.DataStorageManager._create_directory_path')
    @patch('app.services.functions.storages.local_data_storage.DataStorageManager._generate_file_name')
    @patch('app.services.utils.now', return_value="20240101_120000")
    def test_store_data(self, mock_now, mock_generate_file_name, mock_create_directory_path, mock_to_csv):
        mock_generate_file_name.return_value = "filename.csv"
        mock_create_directory_path.return_value = "/some/path"
        data = pd.DataFrame({'column1': [1, 2, 3]})
        file_name = self.manager.store_data(data, "preprocessed_data")
        mock_to_csv.assert_called_once()
        self.assertEqual(file_name, "filename.csv")

    @patch('json.dump')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('app.services.functions.storages.local_data_storage.DataStorageManager._create_directory_path')
    @patch('app.services.functions.storages.local_data_storage.DataStorageManager._generate_file_name')
    @patch('app.services.utils.now', return_value="20240101_120000")
    def test_store_json_data(self, mock_now, mock_generate_file_name, mock_create_directory_path, mock_open, mock_json_dump):
        mock_generate_file_name.return_value = "filename.json"
        mock_create_directory_path.return_value = "/some/path"
        json_data = {"key": "value"}
        file_name = self.manager.store_json_data(json_data, "preprocessed_data")
        mock_json_dump.assert_called_once()
        self.assertEqual(file_name, "filename.json")

    @patch('app.services.functions.managers.logging_manager.LoggingManager.log_error')
    @patch('os.path.isdir', return_value=False)
    def test_get_directory_path_no_folder_mapping(self, mock_isdir, mock_log_error):
        query_name = "non_existing_query"
        data_type = "preprocessed_data"
        # Simulate no folder mapping found
        QueryFolderMapping.get_folder_name = MagicMock(return_value=None)
        dir_path = self.manager._get_directory_path(query_name, data_type)
        self.assertIsNone(dir_path)
        mock_log_error.assert_called_once()

    @patch('app.services.functions.managers.logging_manager.LoggingManager.log')
    @patch('os.path.isdir', return_value=True)
    def test_get_directory_path_success(self, mock_isdir, mock_log):
        query_name = "existing_query"
        data_type = "processed_data"
        expected_dir_path = f"{self.local_storage_dir}/{self.cik_number}/{data_type}/folder_name"
        # Mock folder mapping
        QueryFolderMapping.get_folder_name = MagicMock(return_value="folder_name")
        dir_path = self.manager._get_directory_path(query_name, data_type)
        self.assertEqual(dir_path, expected_dir_path)

    @patch('os.listdir', return_value=[])
    @patch('app.services.functions.storages.local_data_storage.DataStorageManager._get_directory_path', return_value="/some/path")
    @patch('app.services.functions.managers.logging_manager.LoggingManager.log')
    def test_get_latest_file_path_no_files(self, mock_log, mock_get_directory_path, mock_listdir):
        query_name = "query"
        data_type = "preprocessed_data"
        file_path = self.manager.get_latest_file_path(query_name, data_type)
        self.assertIsNone(file_path)
        mock_log.assert_called_with("No files found for query query.", "WARNING")

    @patch('os.path.getmtime', side_effect=lambda x: {'/some/path/file1.csv': 1, '/some/path/file2.csv': 2}[x])
    @patch('os.listdir', return_value=['file1.csv', 'file2.csv'])
    @patch('app.services.functions.storages.local_data_storage.DataStorageManager._get_directory_path', return_value="/some/path")
    def test_get_latest_file_path_success(self, mock_get_directory_path, mock_listdir, mock_getmtime):
        query_name = "query"
        data_type = "processed_data"
        expected_latest_file_path = "/some/path/file2.csv"
        latest_file_path = self.manager.get_latest_file_path(query_name, data_type)
        self.assertEqual(latest_file_path, expected_latest_file_path)

    @patch('app.services.functions.managers.logging_manager.LoggingManager.log_error')
    @patch('os.listdir', side_effect=Exception("Error listing directory"))
    @patch('app.services.functions.storages.local_data_storage.DataStorageManager._get_directory_path', return_value="/some/path")
    def test_get_latest_file_path_exception(self, mock_get_directory_path, mock_listdir, mock_log_error):
        query_name = "query"
        data_type = "processed_data"
        file_path = self.manager.get_latest_file_path(query_name, data_type)
        self.assertIsNone(file_path)
        mock_log_error.assert_called_once()


if __name__ == '__main__':
    unittest.main()
