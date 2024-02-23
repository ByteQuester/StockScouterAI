import numpy as np

from ..base_tables.query_base import FinancialQueryBase


class LiquidityQuery(FinancialQueryBase):

    def __init__(self):
        # Initialize with metrics essential for liquidity analysis
        super().__init__(metrics=['AssetsCurrent', 'LiabilitiesCurrent'])

    def add_calculations(self, df):
        """
        Add liquidity-specific calculations to the DataFrame.
        """
        # Calculate Current Ratio if 'AssetsCurrent' and 'LiabilitiesCurrent' are present
        if 'AssetsCurrent' in df.columns and 'LiabilitiesCurrent' in df.columns:
            df['CurrentRatio'] = np.where(
                df['LiabilitiesCurrent'] > 0,
                round((df['AssetsCurrent'] / df['LiabilitiesCurrent']), 2),
                np.nan  # Use NaN where LiabilitiesCurrent is zero or missing
            )
        return df

    def run_query(self,
                  df,
                  index_cols=None,
                  date_columns=None,
                  rename_map=None):
        """
        Execute the liquidity query process and return the final DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame containing financial data.
            index_cols (list): Columns to use as index in the pivot table.
            date_columns (list): Date columns to convert to datetime.
            rename_map (dict): Optional. A dictionary for renaming columns in the final DataFrame.

        Returns:
            pd.DataFrame: The final DataFrame after executing the query.
        """
        if index_cols is None:
            index_cols = ['EntityName', 'CIK', 'end', 'year', 'quarter']
        if date_columns is None:
            date_columns = ['end']
        if rename_map is None:
            rename_map = {
                'EntityName': 'ENTITY',
                'end': 'DATE',
                'year': 'Year',
                'quarter': 'Quarter',
                'AssetsCurrent': 'CURRENT_ASSETS',
                'LiabilitiesCurrent': 'CURRENT_LIABILITIES',
                'CurrentRatio': 'CURRENT_RATIO'
            }

        # Run the base query process, including preparation, calculations, and renaming
        df_final = super().run_query(df, index_cols, date_columns, rename_map)

        # Scaling and renaming for specific liquidity metrics are handled by the base class and here
        return df_final
