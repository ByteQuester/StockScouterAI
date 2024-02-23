from ..base_tables.query_base import FinancialQueryBase


class CashFlowQuery(FinancialQueryBase):

    def __init__(self):
        # Initialize with metrics essential for cash flow analysis
        super().__init__(metrics=[
            'NetCashProvidedByUsedInOperatingActivities',
            'NetCashProvidedByUsedInInvestingActivities',
            'NetCashProvidedByUsedInFinancingActivities'
        ])

    def add_calculations(self, df):
        # Placeholder for cash flow-specific calculations if needed
        # For this basic implementation, no additional calculations are defined
        return df

    def run_query(self,
                  df,
                  index_cols=None,
                  date_columns=None,
                  rename_map=None):
        """
        Execute the cash flow query process and return the final DataFrame.

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
                'NetCashProvidedByUsedInOperatingActivities':
                'CASH_FLOW_OPERATING',
                'NetCashProvidedByUsedInInvestingActivities':
                'CASH_FLOW_INVESTING',
                'NetCashProvidedByUsedInFinancingActivities':
                'CASH_FLOW_FINANCING'
            }

        # Run the base query process
        df_final = super().run_query(df, index_cols, date_columns, rename_map)

        return df_final
