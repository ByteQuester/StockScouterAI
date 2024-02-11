from typing import List, Union

import pandas as pd

from .processor import FinancialDataProcessor


class AnnualDataProcessor(FinancialDataProcessor):

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the AnnualDataProcessor instance.

        Args:
            df (pd.DataFrame): DataFrame containing the financial data to process.
        """
        super().__init__()
        self.df = df

    def process_data(self, metrics: Union[str, List[str]]) -> pd.DataFrame:
        """
        Processes annually financial data based on specified metrics.

        This method filters, cleans, and sorts the financial data for annual processing based on the given metrics.

        Args:
            metrics (list[str] or str): Financial metrics to process.

        Returns:
            pandas.DataFrame: Processed annually data.
        """
        filtered_df = self.filter_by_metric(self.df, metrics)
        filtered_df = filtered_df[filtered_df['form'] == '10-K']
        filtered_df = filtered_df[filtered_df['frame'].notna()]

        columns_to_drop = ['accn', 'fy', 'fp', 'form', 'filed']
        cleaned_df = self.drop_unnecessary_columns(filtered_df,
                                                   columns_to_drop)

        cleaned_df = self.extract_year(cleaned_df)
        sorted_df = self.sort_dataframe(cleaned_df)

        return sorted_df
