import unittest
from unittest.mock import MagicMock, mock_open, patch

from app.services.utils.file_version_control import FileVersionManager


class TestFileVersionManager(unittest.TestCase):
    @patch('app.services.utils.file_version_control.os.makedirs')
    @patch('app.services.utils.file_version_control.open', new_callable=mock_open, read_data="Existing content")
    def test_update_index(self, mock_open, mock_makedirs):
        # Setup
        base_dir = "/fake/base/dir"
        manager = FileVersionManager(base_dir)

        # Dummy arguments for update_index method
        cik_number = "123456"
        category = "test_category"
        file_name = "test_file.txt"
        storage_type = "test_storage"

        # Call the method under test
        manager.update_index(cik_number, category, file_name, storage_type)

        # Assertions to verify that directories were created and files were written as expected
        mock_makedirs.assert_called_once()
        mock_open.assert_called_once_with(f"{base_dir}/{cik_number}/{storage_type}/index.md", 'w')
        # Add more assertions here to verify the behavior of update_index method

if __name__ == '__main__':
    unittest.main()
