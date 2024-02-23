import numpy as np

from ..base_tables.query_base import FinancialQueryBase


class AssetsLiabilityQuery(FinancialQueryBase):

    def __init__(self):
        super().__init__(metrics=[
            'AssetsCurrent', 'LiabilitiesCurrent', 'StockholdersEquity'
        ])

    def add_calculations(self, df):
        """
        Add specific calculations related to assets and liabilities to the DataFrame.
        """
        # Calculate Asset to Liability Ratio
        if 'AssetsCurrent' in df.columns and 'LiabilitiesCurrent' in df.columns:
            df['AssetToLiabilityRatio'] = np.where(
                df['LiabilitiesCurrent'] != 0,
                round(df['AssetsCurrent'] / df['LiabilitiesCurrent'], 1),
                np.nan)

        # Calculate Debt to Equity Ratio
        if 'LiabilitiesCurrent' in df.columns and 'StockholdersEquity' in df.columns:
            df['DebtToEquityRatio'] = np.where(
                (df['StockholdersEquity'].notna()) &
                (df['LiabilitiesCurrent'].notna()) &
                (df['StockholdersEquity'] != 0),
                round((df['LiabilitiesCurrent'] / df['StockholdersEquity']),
                      1), np.nan)

        return df

    def run_query(self,
                  df,
                  index_cols=None,
                  date_columns=None,
                  rename_map=None):
        """
        Execute the assets and liabilities query process and return the final DataFrame.

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
                'AssetsCurrent': 'ASSETS_CURRENT',
                'LiabilitiesCurrent': 'LIABILITIES_CURRENT',
                'StockholdersEquity': 'STOCKHOLDERS_EQUITY',
                'AssetToLiabilityRatio': 'ASSET_TO_LIABILITY_RATIO',
                'DebtToEquityRatio': 'DEBT_TO_EQUITY_RATIO'
            }

        # Run the base query process
        df_final = super().run_query(df, index_cols, date_columns, rename_map)

        return df_final
