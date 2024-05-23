import pandas as pd


class ProfitabilityFinancialAnalysis:

    def __init__(self, df):
        self.df = df

    def calculate_qoq_growth(self, column_name):
        """Calculates quarter-over-quarter growth for the specified column."""
        if column_name in self.df.columns:
            self.df.sort_values(by=['DATE'], inplace=True)
            self.df[f'{column_name}_QoQ_Growth'] = self.df[
                column_name].pct_change(fill_method=None) * 100
        return self.df

    def calculate_expense_ratio(self):
        """Calculates the expense ratio from revenues and operating income."""
        if all(col in self.df.columns
               for col in ['REVENUES', 'OPS_INCOME_LOSS']):
            self.df['Expense_Ratio'] = (
                self.df['REVENUES'] -
                self.df['OPS_INCOME_LOSS']) / self.df['REVENUES'] * 100
        return self.df

    def calculate_earnings_volatility(self, column_name):
        """Calculates the volatility of specified earnings."""
        if column_name in self.df.columns:
            return self.df[column_name].std()
        return None

    def revenue_distribution_by_quarter(self):
        """Sums up revenues by quarter and retains the ENTITY for coloring."""
        if 'REVENUES' in self.df.columns and 'ENTITY' in self.df.columns:
            return self.df.groupby(['Quarter',
                                    'ENTITY'])['REVENUES'].sum().reset_index()
        return pd.DataFrame()

    def margin_analysis_by_quarter(self):
        """Analyzes profit margins by quarter, including ENTITY for coloring."""
        if 'PROFIT_MARGIN' in self.df.columns and 'ENTITY' in self.df.columns:
            return self.df.groupby(['Quarter', 'ENTITY'
                                    ])['PROFIT_MARGIN'].mean().reset_index()
        return None

    def calculate_yoy_growth(self, column_name):
        """Calculates year-over-year growth for specified column."""
        if column_name in self.df.columns:
            self.df.sort_values(by=['Year', 'Quarter'], inplace=True)
            self.df[f'{column_name}_YoY_Growth'] = self.df.groupby(
                ['Quarter'])[column_name].pct_change(periods=4) * 100
        return self.df

    def calculate_operational_expenses(self):
        """Calculates operational expenses."""
        if all(col in self.df.columns
               for col in ['REVENUES', 'OPS_INCOME_LOSS']):
            self.df['Operational_Expenses'] = self.df['REVENUES'] - self.df[
                'OPS_INCOME_LOSS']
        return self.df


# Example of how to use this class
# csv_data = """Your CSV data here"""
# analysis = BoeingFinancialAnalysis(csv_data)
# analysis.calculate_qoq_growth('REVENUES')
# print(analysis.df)
