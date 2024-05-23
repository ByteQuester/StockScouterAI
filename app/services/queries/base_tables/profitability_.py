import numpy as np

from ..base_tables.query_base import FinancialQueryBase


class ProfitabilityQuery(FinancialQueryBase):

    def __init__(self):
        # Initialize with a list of metrics essential for profitability calculations
        super().__init__(metrics=[
            'NetIncomeLoss', 'OperatingIncomeLoss',
            'RevenueFromContractWithCustomerExcludingAssessedTax'
        ])

    def add_calculations(self, df):
        """
        Add profitability-specific calculations to the DataFrame.
        """
        # Calculate Profit Margin Percent if 'NetIncomeLoss' and 'RevenueFromContractWithCustomerExcludingAssessedTax' are present and not NaN
        if 'NetIncomeLoss' in df.columns and 'RevenueFromContractWithCustomerExcludingAssessedTax' in df.columns:
            df['ProfitMarginPercent'] = np.where(
                (df['NetIncomeLoss'].notna()) &
                (df['RevenueFromContractWithCustomerExcludingAssessedTax'].
                 notna()) &
                (df['RevenueFromContractWithCustomerExcludingAssessedTax']
                 != 0),
                round(
                    (df['NetIncomeLoss'] /
                     df['RevenueFromContractWithCustomerExcludingAssessedTax'])
                    * 100, 2),
                np.nan  # Set to NaN if conditions are not met
            )

        # Example: Implement additional profitability calculations here if needed

        return df

    def run_query(self,
                  df,
                  index_cols=None,
                  date_columns=None,
                  rename_map=None):
        """
        Execute the profitability query process and return the final DataFrame.

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
                'NetIncomeLoss': 'NET_INCOME_LOSS',
                'OperatingIncomeLoss': 'OPS_INCOME_LOSS',
                #DEV
                'RevenueFromContractWithCustomerExcludingAssessedTax':
                'REVENUES',
                'ProfitMarginPercent': 'PROFIT_MARGIN'
            }

        # Run the base query process
        df_final = super().run_query(df, index_cols, date_columns, rename_map)

        return df_final
