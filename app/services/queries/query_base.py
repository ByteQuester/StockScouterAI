from typing import Dict, List

import numpy as np
import pandas as pd


class FinancialQueryBase:

    def __init__(self, metrics: List[str]):
        """
        Initialize the FinancialQueryBase with a list of metrics.

        Args:
            metrics (List[str]): A list of metrics that are essential for the analysis.
        """
        self.metrics = metrics

    def validate_data(self, df: pd.DataFrame,
                      required_columns: List[str]) -> None:
        """
        Check for the presence of required columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing financial data.
            required_columns (List[str]): A list of column names that are required.

        Raises:
            ValueError: If any of the required columns are missing.
        """
        missing_columns = [
            col for col in required_columns if col not in df.columns
        ]
        if missing_columns:
            raise ValueError(
                f"Missing required columns: {', '.join(missing_columns)}")

    def pivot_dataframe(self, df: pd.DataFrame,
                        index_cols: List[str]) -> pd.DataFrame:
        """
        Pivot the DataFrame so that each metric becomes a column, filling missing values with NaN.

        Args:
            df (pd.DataFrame): The DataFrame containing financial data.
            index_cols (List[str]): A list of column names to use as index in the pivot table.

        Returns:
            pd.DataFrame: The pivoted DataFrame.
        """
        pivot_df = df.pivot_table(index=index_cols,
                                  columns='Metric',
                                  values='val',
                                  fill_value=np.nan).reset_index()
        pivot_df.columns.name = None  # Remove MultiIndex
        # Ensure the DataFrame contains all the metrics specified in self.metrics, adding missing ones as NaN
        for metric in self.metrics:
            if metric not in pivot_df:
                pivot_df[metric] = np.nan
        return pivot_df

    def convert_to_datetime(self,
                            df: pd.DataFrame,
                            date_columns: List[str] = ['end']) -> pd.DataFrame:
        """
        Convert specified columns to datetime.

        Args:
            df (pd.DataFrame): The DataFrame containing financial data.
            date_columns (List[str]): A list of column names to convert to datetime.

        Returns:
            pd.DataFrame: The DataFrame with converted date columns.
        """
        for date_column in date_columns:
            df[date_column] = pd.to_datetime(df[date_column])
        return df

    def scale_financial_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Scale financial metrics from cents to millions.

        Args:
            df (pd.DataFrame): The DataFrame containing financial data.

        Returns:
            pd.DataFrame: The DataFrame with scaled financial columns.
        """
        for metric in self.metrics:
            if metric in df.columns:
                df[metric] = df[metric].apply(lambda x: x / 1e6
                                              if pd.notnull(x) else np.nan)
        return df

    def rename_columns(self, df: pd.DataFrame,
                       rename_map: Dict[str, str]) -> pd.DataFrame:
        """
        Rename columns based on the provided mapping.

        Args:
            df (pd.DataFrame): The DataFrame containing financial data.
            rename_map (Dict[str, str]): A dictionary for renaming columns.

        Returns:
            pd.DataFrame: The DataFrame with renamed columns.
        """
        df = df.rename(columns=rename_map)
        return df

    def prepare_data(self,
                     df: pd.DataFrame,
                     index_cols: List[str],
                     date_columns: List[str] = ['end']) -> pd.DataFrame:
        """
        Chain the data preparation steps.

        Args:
            df (pd.DataFrame): The DataFrame containing financial data.
            index_cols (List[str]): A list of column names to use as index in the pivot table.
            date_columns (List[str]): A list of column names to convert to datetime.

        Returns:
            pd.DataFrame: The prepared DataFrame.
        """
        df = self.pivot_dataframe(df, index_cols)
        df = self.convert_to_datetime(df, date_columns)
        df = self.scale_financial_columns(df)
        return df

    def add_calculations(self, df):
        # This method should be overridden by subclasses
        pass

    def run_query(self,
                  df: pd.DataFrame,
                  index_cols: List[str],
                  date_columns: List[str] = ['end'],
                  rename_map: Dict[str, str] = {}) -> pd.DataFrame:
        """
        Execute the query process and return the final DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing financial data.
            index_cols (List[str]): A list of column names to use as index in the pivot table.
            date_columns (List[str]): A column name to convert to datetime. #TODO : dynamic-> date columns + rename_map
            rename_map (Dict[str, str]): A dictionary for renaming columns in the final DataFrame.

        Returns:
            pd.DataFrame: The final DataFrame after executing the query.
        """
        self.validate_data(df, index_cols + ['Metric', 'val'] + date_columns)
        df_final = self.prepare_data(df, index_cols, date_columns)
        df_final = self.add_calculations(df_final)
        df_final = self.rename_columns(df_final, rename_map)
        return df_final
