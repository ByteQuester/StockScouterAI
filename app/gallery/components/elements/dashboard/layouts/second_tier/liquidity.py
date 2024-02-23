import streamlit as st

from app.gallery.components.elements.dashboard.setup.second_tier import \
    FinancialChart
from app.services.queries.dev_tables import LiquidityAnalysis

from .base import SecondTierViewBase


class LiquidityDashboardDev(SecondTierViewBase):

    def __init__(self, cik):
        super().__init__(cik, query_type='Liquidity')
        self.load_data()  # Load data from base class
        # Delay the creation of self.analysis to after data is filtered

    def initialize_analysis(self):
        """Initialize the financial analysis with filtered data."""
        if self.filtered_data is not None:
            self.analysis = LiquidityAnalysis(self.filtered_data)
            self.calculate_metrics(
            )  # Now that analysis is initialized, calculate metrics
            self.generate_insights()
        else:
            raise ValueError("Filtered data is not available for analysis.")

    def calculate_metrics(self):
        """Calculate profitability-specific metrics."""
        self.df_qoq_growth = self.analysis.calculate_qoq_growth(
            'CURRENT_ASSETS')

    def generate_insights(self):
        """Generate insights specific to profitability."""
        self.insights_data = {
            'max_current_assets_growth':
            self.df_qoq_growth['CURRENT_ASSETS_QoQ_Growth'].max(),
            'current_ratio_latest':
            self.filtered_data['CURRENT_RATIO'].iloc[-1]
        }

        self.insights_config = [{
            'title': 'Max Current Assets Growth',
            'data_key': 'max_current_assets_growth',
            'format': '{value:.2f}%'
        }, {
            'title': 'Latest Current Ratio',
            'data_key': 'current_ratio_latest',
            'format': '{value:.2f}'
        }]

        self.data_insights = [{
            'label':
            'Assets Growth Direction',
            'calculation':
            lambda: "Positive" if self.insights_data[
                'max_current_assets_growth'] > 0 else "Negative",
            'positive_outcomes': ['Positive'],
            'explanation':
            'An upward trend in assets indicates the company is expanding its resources, which can support future growth and investment opportunities.'
        }, {
            'label':
            'Liquidity Status',
            'calculation':
            lambda: "Healthy"
            if self.insights_data['current_ratio_latest'] >= 1 else "Risky",
            'positive_outcomes': ['Healthy'],
            'explanation':
            'A healthy liquidity status means the company has enough assets to cover its short-term liabilities, critical for financial stability'
        }]

    def render_charts(self):
        # Display Title and Divider for Key Financial Insights
        st.header('Liquidity Insights')
        st.divider()

        # Render key insights at the top
        self.render_insights(
            insights_type='key')  # Assuming adaptation for selective rendering
        st.divider()

        # ============================ Financial Charts Overview ============================
        st.subheader("Liquidity Charts Overview")
        st.info(
            """Dive into liquidity insights through detailed charts. Each visualization focuses on a critical aspect of the company's liquidity, reflecting its ability to meet short-term obligations and sustain operations."""
        )

        # Main tabs for "Liquidity Overview" and "Dynamic Insights"
        main_tab1, main_tab2 = st.tabs(
            ["Liquidity Overview", "Dynamic Insights"])

        with main_tab1:
            # Sub-tabs for different liquidity aspects
            tab1, tab2, tab3 = st.tabs([
                "Current Assets Growth", "Current Ratio Analysis",
                "Comparative Analysis"
            ])

            # Current Assets Growth Analysis
            with tab1:
                col1, _ = st.columns(
                    [3, 1])  # Adjusting column size for better visualization
                with col1:
                    FinancialChart(
                        chart_type="line",
                        data=self.df_qoq_growth,
                        title=
                        "Quarter-over-Quarter Growth of Current Assets (%)",
                        x_axis="DATE",
                        y_axis="CURRENT_ASSETS_QoQ_Growth").render()

                # Expander for additional insights
                with st.expander("Understanding Current Assets Growth"):
                    st.write("""
                        Tracking the quarter-over-quarter growth of current assets provides insights into the company's operational efficiency and its ability to expand resources. Positive growth signifies an increasing capacity to fund current operations and invest in future growth.
                    """)

            # Current Ratio Analysis
            with tab2:
                col1, _ = st.columns([3, 1])
                if 'CURRENT_RATIO' in self.filtered_data.columns:
                    with col1:
                        FinancialChart(chart_type="line",
                                       data=self.filtered_data,
                                       title="Current Ratio Over Time",
                                       x_axis="DATE",
                                       y_axis="CURRENT_RATIO").render()

                    # Expander for additional insights
                    with st.expander("Understanding the Current Ratio"):
                        st.write("""
                            The Current Ratio is a key liquidity metric that measures a company's ability to pay off its short-term liabilities with its short-term assets. A ratio above 1 indicates a healthy liquidity position, essential for operational stability and financial flexibility.
                        """)

            with tab3:
                selected_metrics = st.multiselect(
                    'Select metrics for comparative analysis:',
                    ['CURRENT_ASSETS', 'CURRENT_LIABILITIES'],
                    default=['CURRENT_ASSETS', 'CURRENT_LIABILITIES'])

                if selected_metrics:
                    FinancialChart(chart_type="line",
                                   data=self.filtered_data,
                                   title="Comparative Analysis Over Time",
                                   x_axis="DATE",
                                   y_axis=selected_metrics).render(
                                       use_container_width=True)

        with main_tab2:
            # Render dynamic insights in a separate tab for detailed analysis
            self.render_insights(insights_type='dynamic')
