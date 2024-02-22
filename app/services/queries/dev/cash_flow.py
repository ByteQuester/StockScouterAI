class CashFlowAnalysis:

    def __init__(self, df):
        self.df = df

    def calculate_yoy_growth(self):
        """Calculates year-over-year growth for cash flow metrics."""
        for column in [
                'CASH_FLOW_FINANCING', 'CASH_FLOW_INVESTING',
                'CASH_FLOW_OPERATING'
        ]:
            if column in self.df.columns and not self.df[column].isnull().any(
            ):
                self.df[f'{column}_YoY'] = self.df[column].pct_change() * 100
        return self.df

    def summary_insights(self):
        """Generates summary insights from the cash flow data."""
        required_columns = [
            'CASH_FLOW_FINANCING', 'CASH_FLOW_INVESTING', 'CASH_FLOW_OPERATING'
        ]
        if all(column in self.df.columns for column in required_columns
               ) and not self.df[required_columns].isnull().any().any():
            self.df['Net_Cash_Flow'] = self.df[required_columns].sum(axis=1)
            self.df['Positive_Cash_Flow'] = self.df['Net_Cash_Flow'] > 0
        return self.df

    def operating_efficiency(self):
        """Assesses the operating efficiency based on operating cash flow."""
        if 'CASH_FLOW_OPERATING' in self.df.columns and not self.df[
                'CASH_FLOW_OPERATING'].isnull().any():
            max_operating_flow = self.df['CASH_FLOW_OPERATING'].max()
            self.df['Operating_Efficiency_Ratio'] = self.df[
                'CASH_FLOW_OPERATING'] / max_operating_flow
        return self.df

    def financing_strategy(self):
        """Analyzes the financing strategy over the years."""
        if 'CASH_FLOW_FINANCING' in self.df.columns and not self.df[
                'CASH_FLOW_FINANCING'].isnull().any():
            self.df['Financing_Strategy'] = self.df[
                'CASH_FLOW_FINANCING'].apply(lambda x: 'Debt Reduction'
                                             if x < 0 else 'Debt Acquisition')
        return self.df

    def investing_trend(self):
        """Identifies trends in investing activities."""
        if 'CASH_FLOW_INVESTING' in self.df.columns and not self.df[
                'CASH_FLOW_INVESTING'].isnull().any():
            self.df['Investing_Trend'] = self.df['CASH_FLOW_INVESTING'].apply(
                lambda x: 'Investing Increase'
                if x > 0 else 'Investing Decrease')
        return self.df


"""# Example usage 
analysis = BoeingCashFlowAnalysis(csv_data)
analysis.calculate_yoy_growth()
analysis.summary_insights()
analysis.operating_efficiency()
analysis.financing_strategy()
analysis.investing_trend()

print(analysis.df.head())"""
