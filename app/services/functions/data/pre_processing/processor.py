from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator, List, Optional, Tuple, Union

import pandas as pd


class FinancialDataProcessor(ABC):
    """
    Abstract base class for processing financial data from SEC filings.

    Provides a structured approach to filtering, transforming, and sorting
    financial data based on predefined metrics. Subclasses must implement the
    `process_data` method tailored to specific financial data processing needs.

    Attributes:
        df (Optional[pd.DataFrame]): A pandas DataFrame storing the financial data to be processed. This
            attribute should be initialized in subclasses.

    Methods:
        process_data(metrics: Union[str, List[str]]): Abstract method. Defines the procedure for processing
            financial data based on specified metrics. Must be implemented by subclasses.
        filter_by_metric(df: pd.DataFrame, metrics: Union[str, List[str]]): Filters the DataFrame by the
            given metrics, returning a subset of the data.
        drop_unnecessary_columns(df: pd.DataFrame, columns_to_drop: List[str]): Removes unwanted columns from
            the DataFrame, streamlining the dataset for further processing.
        sort_dataframe(df: pd.DataFrame): Sorts the DataFrame based on 'year' and 'quarter', facilitating
            ordered analysis and visualization.
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def process_data(self, metrics: Union[str, List[str]]) -> pd.DataFrame:
        """
        Parameters:
            metrics (Union[str, List[str]]): A string or list of strings indicating the financial metrics
                to base the processing on.

        Returns:
            pd.DataFrame: A DataFrame containing the processed financial data.
        """
        pass

    @contextmanager
    def processing_context(self) -> Generator[None, None, None]:
        """
        Context manager for setting up and tearing down the processing environment.
        """
        # TODO: Setup code opening/closing database connection
        yield

    def __call__(self, metrics: Union[str, List[str]]) -> pd.DataFrame:
        """
        Parameters:
            metrics (Union[str, List[str]]): The metrics to process the data by.

        Returns:
            pd.DataFrame: The processed data.
        """
        with self.processing_context():
            return self.process_data(metrics)

    def filter_by_metric(self, df: pd.DataFrame,
                         metrics: Union[str, List[str]]) -> pd.DataFrame:
        """
        Filters the DataFrame by specified metrics.

        Parameters:
            df (pd.DataFrame): The DataFrame to be filtered.
            metrics (Union[str, List[str]]): A string or list of strings representing the metrics
                to filter by.

        Returns:
            pd.DataFrame: The filtered DataFrame containing only the rows that match the specified metrics.
        """
        if isinstance(metrics, str):
            metrics = [metrics]
        return df[df['Metric'].isin(metrics)]

    def drop_unnecessary_columns(self, df: pd.DataFrame,
                                 columns_to_drop: List[str]) -> pd.DataFrame:
        """
        Removes specified columns from a DataFrame.

        Parameters:
            df (pd.DataFrame): The DataFrame from which to drop columns.
            columns_to_drop (List[str]): A list of column names to be removed.

        Returns:
            pd.DataFrame: The DataFrame with the specified columns removed.
        """
        return df.drop(columns=columns_to_drop)

    def extract_year(self,
                     df: pd.DataFrame,
                     frame_col: str = 'frame') -> pd.DataFrame:
        """
        Extracts the year and quarter from a DataFrame column.

        Parameters:
            df (pd.DataFrame): The DataFrame to process.
            frame_col (str, optional): The column name containing date information. Defaults to 'frame'.

        Returns:
            pd.DataFrame: The DataFrame with 'year' and 'quarter' columns added.
        """
        df[['year', 'quarter'
            ]] = df[frame_col].apply(self._custom_sort_key).apply(pd.Series)
        return df.dropna(subset=['year']).drop(columns=[frame_col])

    def extract_quarter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts the quarter from a DataFrame.

        Parameters:
            df (pd.DataFrame): The DataFrame to process.

        Returns:
            pd.DataFrame: The DataFrame with 'year' and 'quarter' columns added.
        """
        df[['year', 'quarter']] = df.apply(self._extract_year_quarter,
                                           axis=1).apply(pd.Series)
        return df.dropna(subset=['year', 'quarter'])

    def sort_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sorts a DataFrame by year and quarter.

        Parameters:
            df (pd.DataFrame): The DataFrame to sort.

        Returns:
            pd.DataFrame: The sorted DataFrame.
        """
        return df.sort_values(by=['year', 'quarter'])

    @staticmethod
    def _custom_sort_key(frame_value: str) -> Tuple[str, int]:
        """
        Custom sort key for sorting records by year and quarter.

        This static method defines a custom sort key used for sorting DataFrame records by year and quarter.
        It extracts the year and quarter information from the 'frame_value' and returns a tuple for sorting.

        Parameters:
            frame_value (str): The value containing year and quarter information.

        Returns:
            Tuple[str, int]: A tuple of year and quarter index for sorting.
        """
        year = frame_value[2:6]
        quarter_order = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4, 'FY': 5}
        quarter = frame_value[6:] if frame_value[6:] in quarter_order else 'FY'
        return year, quarter_order[quarter]

    @staticmethod
    def _extract_year_quarter(row):
        """
        Static method to extract year and quarter from a row.
        """
        if pd.notna(row['frame']) and 'Q' in row['frame']:
            year = row['frame'][2:6]  # Extract year part
            quarter = row['frame'][6:8]  # Extract quarter part
            return [year, quarter]
        return [None, None]  # Exclude non-quarterly entries
