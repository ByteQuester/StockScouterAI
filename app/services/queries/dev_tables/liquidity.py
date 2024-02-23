class LiquidityAnalysis:

    def __init__(self, df):
        self.df = df

    def calculate_qoq_growth(self, column_name):
        """Calculates quarter-over-quarter growth for specified metric, ensuring the metric is available."""
        if column_name in self.df.columns and not self.df[column_name].isnull(
        ).any():
            self.df.sort_values(by=['DATE'], inplace=True)
            self.df[f'{column_name}_QoQ_Growth'] = self.df[
                column_name].pct_change() * 100
        return self.df


"""# Usage example
analysis = BoeingCurrentRatioAnalysis(csv_data)
analysis.verify_current_ratio()
analysis.calculate_qoq_growth('CURRENT_ASSETS')
analysis.calculate_qoq_growth('CURRENT_LIABILITIES')

# To see the DataFrame after calculations
print(analysis.df)"""
