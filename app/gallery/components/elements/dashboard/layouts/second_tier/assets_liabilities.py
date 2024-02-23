import streamlit as st

from app.gallery.components.elements.dashboard.setup import FinancialChart
from app.services.queries.dev_tables import AssetsLiabilitiesEquityAnalysis

from .base import SecondTierViewBase


class AssetsLiabilitiesDashboardDev(SecondTierViewBase):

    def __init__(self, cik):
        super().__init__(cik, query_type='Assets_Liabilities')
        self.load_data()

    def initialize_analysis(self):
        """Initialize the financial analysis with filtered data."""
        if self.filtered_data is not None:
            self.analysis = AssetsLiabilitiesEquityAnalysis(self.filtered_data)
            self.calculate_metrics(
            )  # Now that analysis is initialized, calculate metrics
            self.generate_insights()
        else:
            raise ValueError("Filtered data is not available for analysis.")

    def calculate_metrics(self):
        """Calculate profitability-specific metrics."""
        self.df_qoq_growth = self.analysis.calculate_qoq_growth(
            'ASSETS_CURRENT')
        self.df_working_capital = self.analysis.working_capital()

    def generate_insights(self):
        """Generate insights specific to profitability."""
        self.insights_data = {
            'max_assets_current_growth':
            self.df_qoq_growth['ASSETS_CURRENT_QoQ_Growth'].max(),
            'min_working_capital':
            self.df_working_capital['Working_Capital'].min(),
            'avg_asset_liability_ratio':
            self.filtered_data['ASSET_TO_LIABILITY_RATIO'].mean(),
            'max_debt_equity_ratio':
            self.filtered_data['DEBT_TO_EQUITY_RATIO'].max()
        }

        self.insights_config = [{
            'title': 'Max Growth in Current Assets',
            'data_key': 'max_assets_current_growth',
            'format': '{value:.2f}%'
        }, {
            'title': 'Minimum Working Capital',
            'data_key': 'min_working_capital',
            'format': '${value:,.0f}'
        }, {
            'title': 'Average Asset to Liability Ratio',
            'data_key': 'avg_asset_liability_ratio',
            'format': '{value:.2f}'
        }, {
            'title': 'Maximum Debt to Equity Ratio',
            'data_key': 'max_debt_equity_ratio',
            'format': '{value:.2f}'
        }]

        self.data_insights = [{
            'label':
            'Asset Growth Trend',
            'calculation':
            lambda: "Positive" if self.insights_data[
                'max_assets_current_growth'] > 0 else "Negative",
            'positive_outcomes': ['Positive'],
            'explanation':
            'An asset growth trend that is positive suggests the company is expanding its resource base, potentially increasing its operational capacity and value.'
        }, {
            'label':
            'Financial Stability',
            'calculation':
            lambda: "Stable"
            if self.insights_data['min_working_capital'] > 0 else "Unstable",
            'positive_outcomes': ['Stable'],
            'explanation':
            'Positive working capital indicates the company can cover its short-term liabilities with its short-term assets, signifying financial resilience.'
        }, {
            'label':
            'Leverage Position',
            'calculation':
            lambda: "High"
            if self.insights_data['max_debt_equity_ratio'] > 2 else "Low",
            'positive_outcomes': ['Low'],
            'explanation':
            'A low debt-equity ratio is preferable as it signifies that the company is using less debt and has a lower risk of financial distress.'
        }]

    def render_charts(self):
        # Display Title and Divider for Key Financial Insights
        st.header('Key Financial Insights')
        st.divider()

        # Render key insights at the top
        self.render_insights(
            insights_type='key')  # Assuming adaptation for selective rendering
        st.divider()

        # ============================ Financial Charts Overview ============================
        st.subheader("Financial Charts Overview")
        st.info(
            """Explore comprehensive financial insights through interactive charts. Each chart below represents a key aspect of the company's financial health, enabling a deeper understanding of its financial stability, efficiency, and growth prospects."""
        )

        # Main tabs for "Financial Overview" and "Dynamic Insights"
        main_tab1, main_tab2 = st.tabs(
            ["Financial Overview", "Dynamic Insights"])

        with main_tab1:
            # Sub-tabs for different financial aspects
            tab1, tab2, tab3 = st.tabs([
                "Quarter-over-Quarter Growth", "Asset to Liability Ratio",
                "Comparative Analysis"
            ])

            # Quarter-over-Quarter Growth Analysis
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    FinancialChart(
                        chart_type="line",
                        data=self.df_qoq_growth,
                        title=
                        "Quarter-over-Quarter Growth of Current Assets (%)",
                        x_axis="DATE",
                        y_axis="ASSETS_CURRENT_QoQ_Growth").render()

                with col2:
                    FinancialChart(chart_type="line",
                                   data=self.df_working_capital,
                                   title="Working Capital Over Time",
                                   x_axis="DATE",
                                   y_axis="Working_Capital").render()

                # Expander for additional insights
                with st.expander("Understanding Quarter-over-Quarter Growth"):
                    st.write("""
                       This analysis highlights the company's short-term financial performance by tracking the growth of current assets from one quarter to the next. Positive trends can indicate improving operational efficiency and financial health.
                    """)

            # Expense Ratio Analysis
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    if 'ASSET_TO_LIABILITY_RATIO' in self.filtered_data.columns:
                        FinancialChart(
                            chart_type="line",
                            data=self.filtered_data,
                            title="Asset To Liability Ratio Over Time",
                            x_axis="DATE",
                            y_axis="ASSET_TO_LIABILITY_RATIO").render()

                with col2:
                    if 'DEBT_TO_EQUITY_RATIO' in self.filtered_data.columns:
                        FinancialChart(chart_type="line",
                                       data=self.filtered_data,
                                       title="Debt to Equity Ratio Over Time",
                                       x_axis="DATE",
                                       y_axis="DEBT_TO_EQUITY_RATIO").render()

                # Expander for additional insights
                with st.expander("Understanding Asset to Liability Ratio"):
                    st.write("""
                       The Asset to Liability Ratio is a key indicator of financial stability, reflecting the company's ability to cover its liabilities with its assets. Higher ratios suggest a stronger financial position.
                       The Debt to Equity Ratio measures the company's financial leverage, indicating the proportion of company financing that comes from creditors versus shareholders. Lower ratios are generally preferred, indicating less reliance on debt.
                    """)

            # Profit Margin and Revenue Distribution Analysis
            with tab3:
                selected_metrics = st.multiselect(
                    'Select metrics for comparative analysis:', [
                        'ASSETS_CURRENT', 'LIABILITIES_CURRENT',
                        'STOCKHOLDERS_EQUITY'
                    ],
                    default=['ASSETS_CURRENT', 'LIABILITIES_CURRENT'])

                if selected_metrics:
                    FinancialChart(chart_type="line",
                                   data=self.filtered_data,
                                   title="Comparative Analysis Over Time",
                                   x_axis="DATE",
                                   y_axis=selected_metrics).render(
                                       use_container_width=True)

                # Expander for additional insights
                with st.expander("Understanding Comparative Analysis"):
                    st.write("""
                       Comparative analysis allows for a side-by-side evaluation of key financial metrics over time, aiding in the identification of trends, strengths, and areas of concern within the company's financial performance.
                    """)

        with main_tab2:
            # Render dynamic insights in a separate tab for detailed analysis
            self.render_insights(insights_type='dynamic')
