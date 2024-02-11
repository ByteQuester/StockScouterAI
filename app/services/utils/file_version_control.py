import os


class FileVersionManager:
    """
    Manages versioning and indexing of files in a directory structure.

    Attributes:
        base_dir (str): The base directory path where files are stored.

    Methods:
        update_index(cik_number, category, file_name, storage_type): Updates the index file with file details.
    """

    def __init__(self, base_dir: str):
        """
        Initializes the FileVersionManager with a base directory path.

        Args:
            base_dir (str): The base directory path where files are stored.
        """
        self.base_dir = base_dir

    def update_index(self, cik_number: str, category: str, file_name: str,
                     storage_type: str):
        """
        Updates the index file with new file details for a specific CIK number and storage type.

        Args:
            cik_number (str): The Central Index Key (CIK) number of the company.
            category (str): The category of the data.
            file_name (str): The name of the file to be indexed.
            storage_type (str): The type of storage for the file.
        """
        index_path = os.path.join(self.base_dir, cik_number, storage_type,
                                  'index.md')
        self._write_to_index(index_path, cik_number, category, file_name,
                             storage_type)

    def _write_to_index(self, index_path: str, cik_number: str, category: str,
                        file_name: str, storage_type: str):
        """
        Writes updated content to the index file at the given path.

        Args:
            index_path (str): The path to the index file.
            cik_number (str): The Central Index Key (CIK) number of the company.
            category (str): The category of the data.
            file_name (str): The name of the file to be indexed.
            storage_type (str): The type of storage for the file.
        """
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        index_content = self._read_and_categorize_index(index_path)
        self._update_index_content(index_content, category, file_name,
                                   cik_number, storage_type)
        self._save_index(index_path, cik_number, storage_type, index_content)

    def _update_index_content(self, index_content: dict, category: str,
                              file_name: str, cik_number: str,
                              storage_type: str):
        """
        Updates index content with new file details for a given category.

        Args:
            index_content (dict): The existing index content.
            category (str): The category of the data.
            file_name (str): The name of the file to be indexed.
            cik_number (str): The Central Index Key (CIK) number of the company.
            storage_type (str): The type of storage for the file.
        """
        formatted_category = category.replace(' ', '_')
        relative_path = f"data/{cik_number}/{storage_type}/{formatted_category}/{file_name}"
        category_header = f"### {category}"
        index_content[
            category_header] = f"- [{category} {file_name.split('_')[-1].split('.')[0]}]({relative_path})\n"

    def _read_and_categorize_index(self, index_path: str) -> dict:
        """
        Reads and categorizes lines from the index file into a structured format.

        Args:
            index_path (str): The path to the index file.

        Returns:
            dict: The structured index content.
        """
        if not os.path.exists(index_path):
            return {}

        index_content = {}
        current_category = None
        with open(index_path, 'r') as file:
            for line in file:
                if line.startswith('### '):
                    current_category = line.strip()
                    index_content[current_category] = ''
                elif current_category and line.strip():
                    index_content[current_category] += line
        return index_content

    def _save_index(self, index_path: str, cik_number: str, storage_type: str,
                    index_content: dict):
        """
        Saves the structured index content back to the index file.

        Args:
            index_path (str): The path to the index file.
            cik_number (str): The Central Index Key (CIK) number of the company.
            storage_type (str): The type of storage for the file.
            index_content (dict): The structured index content.
        """
        with open(index_path, 'w') as file:
            self._write_index_header(file, cik_number, storage_type)
            for category, entry in index_content.items():
                file.write(f"{category}\n{entry}\n")

    @staticmethod
    def _write_index_header(file, cik_number, storage_type):
        """
        Writes the header section to the index file.

        Args:
            file: The file object for the index file.
            cik_number (str): The Central Index Key (CIK) number of the company.
            storage_type (str): The type of storage for the file.
        """
        header = f"---\ntitle: CIK {cik_number} Data\nslug: /data/{cik_number}/{storage_type}/\n---\n\n"
        file.write(header)
