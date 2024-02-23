import streamlit as st

from app.gallery.components.elements.dashboard.setup.second_tier import \
    FinancialChart
from app.services.queries.dev_tables import CashFlowAnalysis

from .base import SecondTierViewBase


class CashFlowDashboardDev(SecondTierViewBase):

    def __init__(self, cik):
        super().__init__(cik, query_type='Cash_Flow')
        self.load_data()  # Load data from base class
        # Delay the creation of self.analysis to after data is filtered

    def initialize_analysis(self):
        """Initialize the financial analysis with filtered data."""
        if self.filtered_data is not None:
            self.analysis = CashFlowAnalysis(self.filtered_data)
            self.calculate_metrics(
            )  # Now that analysis is initialized, calculate metrics
            self.generate_insights()
        else:
            raise ValueError("Filtered data is not available for analysis.")

    def calculate_metrics(self):
        """Calculate profitability-specific metrics."""
        self.df_yoy_growth = self.analysis.calculate_yoy_growth()
        self.df_net_flow = self.analysis.summary_insights()
        self.df_operating_efficiency = self.analysis.operating_efficiency()

    def generate_insights(self):
        """Generate insights specific to profitability."""
        self.insights_data = {
            'operating_efficiency_latest':
            self.df_operating_efficiency['Operating_Efficiency_Ratio'].
            iloc[-1],
            'net_cash_flow_latest':
            self.df_net_flow['Net_Cash_Flow'].iloc[-1],
            'positive_cash_flow':
            "Yes" if self.df_net_flow['Positive_Cash_Flow'].iloc[-1] else "No"
        }

        self.insights_config = [{
            'title': 'Latest Operating Efficiency',
            'data_key': 'operating_efficiency_latest',
            'format': '{value:.2f}'
        }, {
            'title': 'Latest Net Cash Flow',
            'data_key': 'net_cash_flow_latest',
            'format': '${value:,.0f}'
        }, {
            'title': 'Positive Cash Flow',
            'data_key': 'positive_cash_flow'
        }]

        self.data_insights = [{
            'label':
            'Cash Flow Health',
            'calculation':
            lambda: "Healthy" if self.insights_data['positive_cash_flow'] ==
            "Yes" else "Concerning",
            'positive_outcomes': ['Healthy'],
            'explanation':
            'Healthy cash flow ensures the company has sufficient funds for operations, investments, and debt payments, key to maintaining solvency.'
        }, {
            'label':
            'Operating Efficiency',
            'calculation':
            lambda: "Optimal" if self.insights_data[
                'operating_efficiency_latest'] > 0.5 else "Needs Improvement",
            'positive_outcomes': ['Optimal'],
            'explanation':
            'High operating efficiency indicates the company is effectively using its resources to generate earnings, vital for long-term success.'
        }]

    def render_charts(self):
        # Display Title and Divider for Cash Flow Insights
        st.header('Cash Flow Insights')
        st.divider()

        # Render key insights at the top
        self.render_insights(
            insights_type='key')  # Assuming adaptation for selective rendering
        st.divider()

        # ============================ Cash Flow Charts Overview ============================
        st.subheader("Cash Flow Charts Overview")
        st.info(
            """Delve into the cash flow insights through interactive charts. This section highlights the company's cash flow from operating, investing, and financing activities, showcasing its financial health and operational efficiency."""
        )

        # Main tabs for "Cash Flow Overview" and "Dynamic Insights"
        main_tab1, main_tab2 = st.tabs(
            ["Cash Flow Overview", "Dynamic Insights"])

        with main_tab1:
            # Sub-tabs for different cash flow aspects
            tab1, tab2, tab3 = st.tabs([
                "Year-over-Year Cash Flow Growth", "Net Cash Flow Analysis",
                "Comparative Analysis"
            ])

            # Year-over-Year Cash Flow Growth Analysis
            with tab1:
                col1, _ = st.columns(
                    [3, 1])  # Adjusting column size for better visualization
                with col1:
                    for column in [
                            'CASH_FLOW_FINANCING_YoY',
                            'CASH_FLOW_INVESTING_YoY',
                            'CASH_FLOW_OPERATING_YoY'
                    ]:
                        if column in self.df_yoy_growth.columns:
                            FinancialChart(
                                chart_type="line",
                                data=self.df_yoy_growth,
                                title=f'Year-over-Year Growth: {column}',
                                x_axis="DATE",
                                y_axis=column,
                                labels={
                                    column: 'Growth (%)'
                                }).render()

                # Expander for additional insights
                with st.expander(
                        "Understanding Year-over-Year Cash Flow Growth"):
                    st.write("""
                        Analyzing the year-over-year growth in cash flow from financing, investing, and operating activities provides insights into the company's financial dynamics. Positive growth in operating cash flow is particularly indicative of healthy operational efficiency.
                    """)

            # Net Cash Flow Analysis
            with tab2:
                col1, _ = st.columns([3, 1])
                if 'Net_Cash_Flow' in self.df_net_flow.columns:
                    with col1:
                        FinancialChart(chart_type="bar",
                                       data=self.df_net_flow,
                                       title="Net Cash Flow Over Time",
                                       color='Positive_Cash_Flow',
                                       labels={
                                           'Net_Cash_Flow': 'Net Cash Flow'
                                       },
                                       x_axis="DATE",
                                       y_axis='Net_Cash_Flow').render()

                    # Expander for additional insights
                    with st.expander("Understanding Net Cash Flow"):
                        st.write("""
                            Net cash flow reflects the total amount of money being transferred into and out of a company's accounts, influenced by its operating, investing, and financing activities. Consistently positive net cash flow is crucial for long-term financial health.
                        """)

            with tab3:
                selected_metrics = st.multiselect(
                    'Select metrics for comparative analysis:', [
                        'CASH_FLOW_FINANCING', 'CASH_FLOW_INVESTING',
                        'CASH_FLOW_OPERATING'
                    ],
                    default=[
                        'CASH_FLOW_FINANCING', 'CASH_FLOW_INVESTING',
                        'CASH_FLOW_OPERATING'
                    ])

                if selected_metrics:
                    FinancialChart(chart_type="line",
                                   data=self.filtered_data,
                                   title="Comparative Analysis Over Time",
                                   x_axis="DATE",
                                   y_axis=selected_metrics,
                                   labels={
                                       metric: metric.replace('_',
                                                              ' ').title()
                                       for metric in selected_metrics
                                   }).render(use_container_width=True)

        with main_tab2:
            # Render dynamic insights in a separate tab for detailed analysis
            self.render_insights(insights_type='dynamic')
