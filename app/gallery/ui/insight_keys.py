import streamlit as st


class KeyInsights:

    def __init__(self, data, insights_config):
        """
        Initializes the KeyInsights class with data and a configuration for insights.

        :param data: A dictionary containing the data needed for insights.
        :param insights_config: A list of dictionaries where each dictionary specifies
                                an insight's title and the corresponding data key.
        """
        self.data = data
        self.insights_config = insights_config

    def render(self):
        columns = st.columns(len(self.insights_config))
        for col, insight in zip(columns, self.insights_config):
            title = insight.get('title')
            data_key = insight.get('data_key')
            value_format = insight.get('format',
                                       '{value:,.0f}')  # Default format
            value = self.data.get(data_key, 'N/A')

            # Check if value is numeric and format accordingly
            if isinstance(value, (int, float)) and value != 'N/A':
                formatted_value = value_format.format(value=value)
            else:
                # For non-numeric values, bypass numeric formatting
                formatted_value = value

            col.markdown(self._insight_box(title, formatted_value),
                         unsafe_allow_html=True)

    def _insight_box(self, title, value):
        """
        Generates HTML for an insight box.

        :param title: The title of the insight.
        :param value: The value of the insight.
        :return: A string containing HTML for the insight box.
        """
        return f"""<div class='insight-box'><h4>{title}</h4><p>{value}</p></div>"""


"""# Assuming 'data' is a dictionary containing relevant financial data
data = {
    'total_assets': 1000000,
    'total_liabilities': 500000,
    'current_ratio': 2.0,
    'profit_margin': "10%"
}

# Configure insights to be displayed
insights_config = [
    {'title': 'Total Assets', 'data_key': 'total_assets'},
    {'title': 'Total Liabilities', 'data_key': 'total_liabilities'},
    {'title': 'Current Ratio', 'data_key': 'current_ratio', 'format': '{value:.2f}'},
    {'title': 'Profit Margin', 'data_key': 'profit_margin'}
]

key_insights = KeyInsights(data, insights_config)
key_insights.render()
"""
