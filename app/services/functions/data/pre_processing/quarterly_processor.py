from typing import List, Union

import pandas as pd

from .processor import FinancialDataProcessor


class QuarterlyDataProcessor(FinancialDataProcessor):

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the QuarterlyDataProcessor instance.

        Args:
            df (pd.DataFrame): DataFrame containing the quarterly financial data to process.
        """
        super().__init__()
        self.df = df

    def process_data(self, metrics: Union[str, List[str]]) -> pd.DataFrame:
        """
        Processes quarterly financial data based on specified metrics.

        This method filters, cleans, and sorts the quarterly financial data based on the given metrics.

        Args:
            metrics (list[str] or str): Financial metrics to process.

        Returns:
            pandas.DataFrame: Processed quarterly data.
        """
        filtered_df = self.filter_by_metric(self.df, metrics)

        columns_to_drop = ['accn', 'form', 'filed']
        cleaned_df = self.drop_unnecessary_columns(filtered_df,
                                                   columns_to_drop)

        cleaned_df = self.extract_quarter(cleaned_df)
        sorted_df = self.sort_dataframe(cleaned_df)
        sorted_df = sorted_df.drop(columns=['frame', 'fp', 'fy'])

        return sorted_df
