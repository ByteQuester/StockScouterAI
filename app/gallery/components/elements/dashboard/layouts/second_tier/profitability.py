import streamlit as st

from app.gallery.components.elements.dashboard.setup.second_tier import \
    FinancialChart
from app.services.queries.dev import ProfitabilityFinancialAnalysis

from .base import SecondTierViewBase


#    st.markdown(f"### Earnings Volatility (Standard Deviation): {earnings_volatility:.2f}") need added
class ProfitabilityDashboardDev(SecondTierViewBase):

    def __init__(self, cik):
        super().__init__(cik, query_type='Profitability')
        self.load_data()  # Load data from base class
        # Delay the creation of self.analysis to after data is filtered

    def initialize_analysis(self):
        """Initialize the financial analysis with filtered data."""
        if self.filtered_data is not None:
            self.analysis = ProfitabilityFinancialAnalysis(self.filtered_data)
            self.calculate_metrics(
            )  # Now that analysis is initialized, calculate metrics
            self.generate_insights()
        else:
            raise ValueError("Filtered data is not available for analysis.")

    def calculate_metrics(self):
        """Calculate profitability-specific metrics."""
        self.df_qoq_growth = self.analysis.calculate_qoq_growth('REVENUES')
        self.df_expense_ratio = self.analysis.calculate_expense_ratio()
        self.df_revenue_distribution = self.analysis.revenue_distribution_by_quarter(
        ).reset_index()
        self.df_yoy_growth = self.analysis.calculate_yoy_growth(
            'NET_INCOME_LOSS')
        self.df_margin_analysis = self.analysis.margin_analysis_by_quarter(
        ).reset_index()
        self.earnings_volatility = self.analysis.calculate_earnings_volatility(
            'NET_INCOME_LOSS')

    def generate_insights(self):
        """Generate insights specific to profitability."""
        self.insights_data = {
            'max_revenue_growth':
            self.df_qoq_growth['REVENUES_QoQ_Growth'].max(),
            'avg_profit_margin':
            self.df_margin_analysis['PROFIT_MARGIN'].mean(),
            'min_expense_ratio':
            self.df_expense_ratio['Expense_Ratio'].min(),
            'max_net_income_growth':
            self.df_yoy_growth['NET_INCOME_LOSS_YoY_Growth'].max()
        }

        self.insights_config = [{
            'title': 'Max Revenue Growth',
            'data_key': 'max_revenue_growth',
            'format': '{value:.2f}%'
        }, {
            'title': 'Average Profit Margin',
            'data_key': 'avg_profit_margin',
            'format': '{value:.2f}%'
        }, {
            'title': 'Minimum Expense Ratio',
            'data_key': 'min_expense_ratio',
            'format': '{value:.2f}%'
        }, {
            'title': 'Max Net Income Growth',
            'data_key': 'max_net_income_growth',
            'format': '{value:.2f}%'
        }]

        self.data_insights = [{
            'label':
            'Revenue Growth Trend',
            'calculation':
            lambda: "Positive"
            if self.insights_data['max_revenue_growth'] > 0 else "Negative",
            'positive_outcomes': ['Positive'],
            'explanation':
            'A positive revenue growth trend indicates the company is increasing its sales over time, reflecting potential market expansion and customer base growth.'
        }, {
            'label':
            'Profit Margin Stability',
            'calculation':
            lambda: "Stable"
            if self.insights_data['avg_profit_margin'] >= 5 else "Volatile",
            'positive_outcomes': ['Stable'],
            'explanation':
            'Stability in profit margins suggests the company can consistently retain a portion of its sales as profits, indicating financial health and operational efficiency.'
        }, {
            'label':
            'Expense Management',
            'calculation':
            lambda: "Efficient"
            if self.insights_data['min_expense_ratio'] < 50 else "Inefficient",
            'positive_outcomes': ['Efficient'],
            'explanation':
            ' Efficient expense management shows the company is capable of controlling its costs relative to its income, ensuring sustainable operations.'
        }, {
            'label':
            'Net Income Growth Direction',
            'calculation':
            lambda: "Growing" if self.insights_data['max_net_income_growth'] >
            0 else "Declining",
            'positive_outcomes': ['Growing'],
            'explanation':
            'Positive net income growth signifies the company is improving its profitability over time, an indicator of strong financial performance.'
        }]

    def render_charts(self):
        # Display Title
        st.header('Profitability Insights')
        st.divider()
        self.render_insights(insights_type='key')
        st.divider()
        # ============================  Plots  ============================
        st.subheader("Profitability Charts Overview")
        st.info(
            """Explore comprehensive financial insights through interactive charts. Each chart below represents a key aspect of the company's financial health, enabling a deeper understanding of its financial stability, efficiency, and growth prospects"""
        )
        main_tab1, main_tab2 = st.tabs(
            ["Financial Overview", "Dynamic Insights"])
        with main_tab1:
            tab1, tab2, tab3, tab4 = st.tabs([
                "Quarter-over-Quarter Growth", "Expense Ratio Analysis",
                "Profit Margin & Revenue Distribution", "Comparative Analysis"
            ])

            # Quarter-over-Quarter Growth Analysis
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    FinancialChart(
                        chart_type="line",
                        data=self.df_qoq_growth,
                        title="Quarter-over-Quarter Revenue Growth (%)",
                        x_axis="DATE",
                        y_axis="REVENUES_QoQ_Growth").render()
                with col2:
                    if 'PROFIT_MARGIN' in self.filtered_data.columns:
                        FinancialChart(
                            chart_type="line",
                            data=self.filtered_data,
                            title="Profit Margin Analysis by Quarter (%)",
                            x_axis="DATE",
                            y_axis="PROFIT_MARGIN").render()

                with st.expander("Understanding Quarter-over-Quarter Growth"):
                    st.write("""
                        Quarter-over-Quarter growth analysis allows us to understand the short-term financial trajectory of the company.
                        A consistent increase in revenue growth percentage indicates a positive market response and operational efficiency.
                    """)

            # Expense Ratio Analysis
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    FinancialChart(chart_type="scatter",
                                   data=self.df_expense_ratio,
                                   title="Expense Ratio Over Time (%)",
                                   x_axis="DATE",
                                   y_axis="Expense_Ratio").render()
                with col2:
                    st.empty()  # Placeholder for future charts or insights

                with st.expander("Understanding Expense Ratio"):
                    st.write("""
                        The expense ratio indicates how much of a company's revenue is consumed by operational and non-operational expenses.
                        Lower ratios suggest higher efficiency, while higher ratios may indicate potential overspending or operational inefficiencies.
                    """)

            # Profit Margin and Revenue Distribution Analysis
            with tab3:
                col1, col2 = st.columns(2)
                with col1:
                    FinancialChart(chart_type="bar",
                                   data=self.df_revenue_distribution,
                                   title="Revenue Distribution by Quarter",
                                   x_axis="Quarter",
                                   y_axis="REVENUES").render()
                with col2:
                    FinancialChart(
                        chart_type="bar",
                        data=self.df_margin_analysis,
                        title="Profit Margin Analysis by Quarter (%)",
                        x_axis="Quarter",
                        y_axis="PROFIT_MARGIN").render()

                with st.expander(
                        "Understanding Profit Margins & Revenue Distribution"):
                    st.write("""
                        Analyzing profit margins in conjunction with revenue distribution provides a holistic view of the company's financial health.
                        This combined analysis can uncover trends in profitability against revenue streams over different quarters, highlighting areas of strength and concern.
                    """)
            with tab4:
                selected_metrics = st.multiselect(
                    'Select metrics for comparative analysis:',
                    ['NET_INCOME_LOSS', 'OPS_INCOME_LOSS', 'REVENUES'],
                    default=['NET_INCOME_LOSS', 'OPS_INCOME_LOSS', 'REVENUES'])

                if selected_metrics:
                    FinancialChart(chart_type="line",
                                   data=self.filtered_data,
                                   title="Comparative Analysis Over Time",
                                   x_axis="DATE",
                                   y_axis=selected_metrics).render(
                                       use_container_width=True)

                # Expander for additional insights
                with st.expander(
                        "Understanding Profit Margins & Revenue Distribution"):
                    st.write("""
                        This analysis combines profit margins with revenue distribution to offer a comprehensive view of financial health, 
                        revealing patterns in profitability and revenue streams across different periods.
                    """)

        with main_tab2:
            # Render dynamic insights in a separate tab
            self.render_insights(insights_type='dynamic')
