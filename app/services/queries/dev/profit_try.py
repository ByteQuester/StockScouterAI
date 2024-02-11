import numpy as np
import pandas as pd
from queries.query_base import FinancialQueryBase


class ProfitabilityQuery(FinancialQueryBase):

    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare and preprocess the financial data.

        Args:
            df (pd.DataFrame): The input DataFrame containing financial data.

        Returns:
            pd.DataFrame: The preprocessed DataFrame.
        Example:
        Prepare and preprocess financial data
        >>> query = ProfitabilityQuery()
        >>> sample_data = pd.DataFrame({
        >>>     'EntityName': ['BOEING CO', 'BOEING CO', 'BOEING CO'],
        >>>     'CIK': [12927, 12927, 12927],
        >>>     'Metric': ['NetIncomeLoss', 'OperatingIncomeLoss', 'Revenues'],
        >>>     'end': ['2014-03-31', '2014-03-31', '2014-03-31'],
        >>>     'val': [965000000, 1542000000, 20465000000],
        >>>     'start': ['2014-01-01', '2014-01-01', '2014-01-01'],
        >>>     'year': [2014, 2014, 2014],
        >>>     'quarter': ['Q1', 'Q1', 'Q1']
        >>> })
        >>> processed_data = query.prepare_data(sample_data)
        >>> print(processed_data)
        """
        required_columns = [
            'EntityName', 'CIK', 'Metric', 'end', 'val', 'start', 'year',
            'quarter'
        ]
        missing_columns = [
            col for col in required_columns if col not in df.columns
        ]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        df_final = (df.pipe(
            self.pivot_dataframe,
            index_cols=[
                'EntityName', 'CIK', 'end', 'year', 'quarter', 'start'
            ],
            columns_col='Metric',
            values_col='val').pipe(self.convert_to_datetime, 'end').pipe(
                self.convert_cents_to_millions,
                ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']))
        return df_final

    def calculate_profit_margin(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate the profit margin and add it to the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame with financial data.

        Returns:
            pd.DataFrame: The DataFrame with added profit margin.
        """
        df['ProfitMarginPercent'] = np.where(
            (df['NetIncomeLoss'].notna()) & (df['Revenues'].notna()) &
            (df['Revenues'] != 0),
            round((df['NetIncomeLoss'] / df['Revenues']) * 100, 2), None)
        return df

    def compute_rolling_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute rolling averages for specific columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame with financial data.

        Returns:
            pd.DataFrame: The DataFrame with added rolling averages.
        """
        return df.pipe(
            self.calculate_rolling_average,
            group_by_cols=['EntityName', 'CIK'],
            target_cols=['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss'])

    def calculate_growth_rates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate growth rates for specific columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame with financial data.

        Returns:
            pd.DataFrame: The DataFrame with added growth rates.
        """
        for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']:
            df = df.pipe(self.calculate_pct_change, ['EntityName', 'CIK'],
                         f'{col}_RollingAvg')
        return df

    def categorize_growth_rates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize growth rates in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame with financial data.

        Returns:
            pd.DataFrame: The DataFrame with categorized growth rates.
        """
        for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']:
            df = df.apply(
                lambda row: self.categorize_growth(row[f'{col}_QoQ']), axis=1)
        return df

    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize data in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame with financial data.

        Returns:
            pd.DataFrame: The DataFrame with normalized data.
        """
        for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']:
            df[f'{col}_Normalized'] = df.groupby([
                'year', 'quarter'
            ])[f'{col}_QoQ_Growth'].apply(lambda x: (x - x.mean()) / x.std())
        return df

    def structure_final_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Structure the final DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame with financial data.

        Returns:
            pd.DataFrame: The structured final DataFrame.
        """
        columns_to_select = ['EntityName', 'CIK', 'end', 'NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss',
                             'ProfitMarginPercent', 'year', 'quarter'] + \
                            [f'{col}_RollingAvg' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']] #+ \
        #[f'{col}_QoQ' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']] + \
        #[f'{col}_QoQ_Category' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']] + \
        #[f'{col}_QoQ_Growth' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']] + \
        #[f'{col}_Normalized' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']]
        df_final = df[columns_to_select]
        df_final = self.rename_columns(
            df_final, {
                'EntityName': 'ENTITY',
                'end': 'DATE',
                'year': 'Year',
                'quarter': 'Quarter'
            })
        return df_final

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Execute the entire query process and return the final DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame containing financial data.

        Returns:
            pd.DataFrame: The final DataFrame after executing the query.
        """
        df_final = (
            df.pipe(self.prepare_data).pipe(self.calculate_profit_margin).pipe(
                self.compute_rolling_averages)
            #.pipe(self.calculate_growth_rates)
            #.pipe(self.categorize_growth_rates)
            #.pipe(self.normalize_data)
            .pipe(self.structure_final_data))
        return df_final
