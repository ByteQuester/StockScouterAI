import os


class FilePaths:

    def __init__(self,
                 default_stage_name='TEST_STAGE',
                 default_table_name='TEST_TABLE'):
        self.DEFAULT_STAGE_NAME = default_stage_name
        self.DEFAULT_TABLE_NAME = default_table_name
        self.CSV_DIRECTORY = 'data'

        if not os.path.exists(self.CSV_DIRECTORY):
            os.makedirs(self.CSV_DIRECTORY)

        self.CSV_FILE_PATH = os.path.join(self.CSV_DIRECTORY, 'data.csv')
