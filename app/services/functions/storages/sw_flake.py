"""
This class manages connections and data operations with Snowflake.
It handles establishing a connection to Snowflake, uploading data,
executing queries, including those from SQL files, and closing the connection.
"""
# TODO: Dynamic Handling of Stage and Table Names
# TODO: automate schema detection and table creation from data input
# TODO: support to include additional file formats
# TODO: documentation with detailed descriptions and usage examples
# TODO: Snowflake Stage Existence and Authorization Check
# TODO: Enhanced error handling
#  This class is our humble attempt to bring data to the table (quite literally).

import os

import pandas as pd
from snowflake import connector

from app.services.configs import SnowflakeConfig
from app.services.functions.managers import LoggingManager
from app.services.types import CSV_FILE_PATH, DEFAULT_TABLE_NAME
from app.services.utils import dataframe_to_csv


class SnowflakeDataManager:

    def __init__(self,
                 config: SnowflakeConfig,
                 custom_table_name=None,
                 custom_stage_name=None):
        """
        Initializes the SnowflakeDataManager class.
        Args:
            custom_table_name (str): Custom table name provided by the user.
            custom_stage_name (str): Custom stage name provided by the user.
        """
        self.user = config.user
        self.password = config.password
        self.account = config.account
        self.warehouse = config.warehouse
        self.database = config.database
        self.schema = config.schema
        self.port = config.port
        self.role = config.role
        # Establish a connection
        self.connection = None
        self.connect_to_snowflake()
        # Initialize other classes
        self.error_handler = LoggingManager()
        # Set custom table and stage names
        self.custom_table_name = custom_table_name
        self.custom_stage_name = custom_stage_name

    def connect_to_snowflake(self):
        """
        Establishes a connection to Snowflake using environment variables for credentials.
        Raises:
            Exception: If there is an error in connecting to Snowflake.
        """
        try:
            self.connection = connector.connect(
                user=self.user,
                password=self.password,
                account=self.account,
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema,
                port=self.port,
                role=self.role,
            )
        except Exception as e:
            print(f"Error connecting to Snowflake: {e}")
            raise

    def upload_data(self, data, table_name=None):
        """
        Converts a pandas DataFrame to CSV and uploads it to Snowflake.

        Args:
            data (pd.DataFrame): The DataFrame to upload.
            table_name (str): The name of the Snowflake table. If None, uses the default table name.
        """
        if self.connection is None or data.empty:
            self.error_handler.log(
                "No connection to Snowflake or data is empty.", "ERROR")
            return

        try:
            # Convert DataFrame to CSV
            dataframe_to_csv(data, CSV_FILE_PATH)

            # Determine the table name
            table_name = table_name or DEFAULT_TABLE_NAME

            # Generate the stage name for PUT command
            put_stage_name = self._generate_stage_name(table_name, 'PUT')

            # Upload CSV to Snowflake Stage
            self.put_file_to_stage(CSV_FILE_PATH, put_stage_name)

            # Delete the local CSV file after upload
            try:
                os.remove(CSV_FILE_PATH)
                print(f"Temporary file {CSV_FILE_PATH} deleted successfully.")
            except Exception as e:
                self.error_handler.log(f"Error deleting temporary file: {e}",
                                       "ERROR")

            # Generate the stage name for COPY command
            copy_stage_name = self._generate_stage_name(table_name, 'COPY')

            # Copy data from stage to table
            self.copy_data_from_stage_to_table(copy_stage_name, table_name)
        except Exception as e:
            self.error_handler.log(f"Error in upload process: {e}", "ERROR")

    def put_file_to_stage(self, file_path, stage_name=None):
        """
        Uploads a file from the local filesystem to the specified Snowflake stage.

        Args:
            file_path (str): The local path to the file to upload.
            stage_name (str): The name of the Snowflake stage to upload the file to.
                              If None, a stage name is generated.
        """
        if self.connection is None:
            self.error_handler.log("No connection to Snowflake.", "ERROR")
            return

        try:
            # Generate the stage name using the provided or default table name
            stage_name = stage_name or self._generate_stage_name(
                DEFAULT_TABLE_NAME, 'PUT')

            with self.connection.cursor() as cursor:
                put_command = f"PUT file://{file_path} {stage_name} AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
                cursor.execute(put_command)
                print(f"File {file_path} uploaded to stage {stage_name}")
        except Exception as e:
            self.error_handler.log(
                f"Error uploading file to Snowflake stage: {e}", "ERROR")

    def copy_data_from_stage_to_table(self, stage_name=None, table_name=None):
        """
        Copies data from a specified Snowflake stage to a Snowflake table.

        Args:
            stage_name (str): The name of the Snowflake stage. If None, a stage name is generated.
            table_name (str): The name of the Snowflake table. If None, uses the default table name.
        """
        if self.connection is None:
            self.error_handler.log("No connection to Snowflake.", "ERROR")
            return

        try:
            # Generate the stage name using the provided or default table name
            stage_name = stage_name or self._generate_stage_name(
                table_name, 'COPY')

            # Use the provided or default table name
            table_name = table_name or DEFAULT_TABLE_NAME

            with self.connection.cursor() as cursor:
                copy_command = f"COPY INTO {table_name} FROM {stage_name} FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '\"' SKIP_HEADER = 1)"
                cursor.execute(copy_command)
                print(
                    f"Data copied from stage {stage_name} to table {table_name}"
                )
        except Exception as e:
            self.error_handler.log(
                f"Error copying data from stage to table: {e}", "ERROR")

    def get_data(self, query):
        """
        Executes a SQL query in Snowflake and returns the results.
        Args:
            query (str): The SQL query to execute.
        Returns:
            pd.DataFrame: The results of the query as a pandas DataFrame.
        """
        if self.connection is None:
            self.error_handler.log("No connection to Snowflake.", "ERROR")
            return pd.DataFrame()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                # Convert the result into a pandas DataFrame
                df = pd.DataFrame(
                    result, columns=[col[0] for col in cursor.description])
                return df
        except Exception as e:
            self.error_handler.log(f"Error executing query in Snowflake: {e}",
                                   "ERROR")
            return pd.DataFrame()

    def execute_query_from_file(self, query_filename):
        """
        Executes a SQL query from a file.
        Args:
            query_filename (str): The path to the SQL file containing the query.
        Returns:
            list: The results of the SQL query.
        """
        with open(query_filename, 'r') as file:
            query = file.read()
        return self.get_data(query)

    def close_connection(self):
        """
        Closes the connection to Snowflake.
        """
        if self.connection:
            self.connection.close()
            print("Connection to Snowflake closed successfully.")

    def create_table(self, table_name):
        """
        Creates a table in Snowflake with specific columns.
        Args:
            table_name (str): The name of the table to create.
        """
        try:
            cursor = self.connection.cursor()
            sql = f"""
                   CREATE TABLE {self.schema}.{table_name} (
                       EntityName VARCHAR(255),
                       CIK INT,
                       Metric VARCHAR(255),
                       End DATE,
                       Value FLOAT,
                       accn VARCHAR(255),
                       fy INT,
                       fp VARCHAR(10),
                       form VARCHAR(10),
                       filed DATE,
                       frame VARCHAR(50),
                       start DATE
                   )
                   """
            cursor.execute(sql)
            self.connection.commit()
            print(
                f"Table {table_name} created successfully with specific columns."
            )
        except Exception as e:
            self.error_handler.log(f"Error creating table: {e}", "ERROR")

    def _generate_stage_name(self, table_name=None, command_type='COPY'):
        """
        Generates the appropriate stage name based on the command type.
        Note: Normally, the stage name for COPY should be '@table_name', but '@%table_name'
        has been found to work more effectively in our specific environment. This deviation
        from the standard practice is intentional and should be reviewed if there are future
        updates to the Snowflake platform or issues in stage handling.

        Args:
            table_name (str): The name of the Snowflake table. If None, uses the default table name.
            command_type (str): The type of command ('PUT' or 'COPY').

        Returns:
            str: The formatted stage name.
        """
        if table_name is None:
            table_name = DEFAULT_TABLE_NAME

        if command_type == 'PUT':
            return f"@%{table_name}"
        elif command_type == 'COPY':
            return f"@%{table_name}"
        else:
            self.error_handler.log(f"Invalid command type: {command_type}",
                                   "ERROR")
            return None
