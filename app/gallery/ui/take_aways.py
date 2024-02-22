import streamlit as st


class DynamicInsights:

    def __init__(self, data_insights):
        """
        Initializes the DynamicInsights class with data insights.

        :param data_insights: A list of dictionaries, each containing the data needed for an insight.
        """
        self.data_insights = data_insights

    def render(self):
        for insight in self.data_insights:
            trend = insight['calculation']()
            color = "green" if trend in insight['positive_outcomes'] else "red"
            explanation = insight.get('explanation',
                                      '')  # Fetch explanation if exists
            self._render_insight(insight['label'], trend, color, explanation)

    def _render_insight(self, label, trend, color, explanation):
        """
        Renders a single insight with dynamic color based on its trend.

        :param label: The label for the insight.
        :param trend: The trend value for the insight.
        :param color: The color code based on the trend.
        """
        st.markdown(f"**{label}**: ", unsafe_allow_html=True)
        st.markdown(
            f"The {label.lower()} is <span style='color:{color};'>{trend}</span>.",
            unsafe_allow_html=True)
        explanation_colored = self._add_color_to_keywords(explanation)
        st.markdown(explanation_colored, unsafe_allow_html=True)

    def _add_color_to_keywords(self, text):
        """
        Adds color to important keywords in the explanation text.

        :param text: The explanation text.
        :return: The explanation with colored keywords.
        """
        # Define keywords and their associated colors
        keywords = {
            'Positive': 'green',
            'Negative': 'red',
            'Stable': 'blue',
            'Unstable': 'red',
            'High': 'red',
            'Low': 'green',
            'Healthy': 'green',
            'Concerning': 'red',
            'Optimal': 'green',
            'Needs Improvement': 'red',
            'Efficient': 'green',
            'Inefficient': 'red',
            'Growing': 'green',
            'Declining': 'red'
        }

        # Replace keywords with colored span elements
        for keyword, color in keywords.items():
            text = text.replace(
                keyword, f"<span style='color:{color};'>{keyword}</span>")

        return text


"""# Example usage:

# Assuming 'df_profitability', 'df_cash_flow', 'df_liquidity', and 'df_assets_liabilities' are your DataFrame variables.
data_insights = [
    {
        'label': 'Profit Margin Trend',
        'calculation': lambda: "increasing" if df_profitability['PROFIT_MARGIN'].iloc[-1] > df_profitability['PROFIT_MARGIN'].iloc[0] else "decreasing",
        'positive_outcomes': ['increasing'],
    },
    {
        'label': 'Cash Flow Health',
        'calculation': lambda: "healthy" if df_cash_flow['CASH_FLOW_OPERATING'].iloc[-1] > 0 else "concerning",
        'positive_outcomes': ['healthy'],
    },
    {
        'label': 'Liquidity Position',
        'calculation': lambda: "good" if df_liquidity['CURRENT_RATIO'].iloc[-1] > 1 else "poor",
        'positive_outcomes': ['good'],
    },
    {
        'label': 'Leverage Situation',
        'calculation': lambda: "increasing risk" if df_assets_liabilities['DEBT_TO_EQUITY_RATIO'].iloc[-1] > df_assets_liabilities['DEBT_TO_EQUITY_RATIO'].iloc[0] else "stable",
        'positive_outcomes': ['stable'],
    },
]

dynamic_insights = DynamicInsights(data_insights)
dynamic_insights.render()
"""
