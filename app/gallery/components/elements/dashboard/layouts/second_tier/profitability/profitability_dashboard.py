import streamlit as st

from app.gallery.components.elements.dashboard.setup import render_chart
from app.gallery.ui import UIHelpers
from app.services.queries.dev_tables import ProfitabilityFinancialAnalysis

from ..base import SecondTierViewBase
from .graph_renderers import *


class ProfitabilityDashboardDev(SecondTierViewBase):

    def __init__(self, cik):
        super().__init__(cik, query_type='Profitability')
        self.load_data()  # Load data from base class

    def initialize_analysis(self):
        """Initialize the financial analysis with filtered data."""
        if self.filtered_data is not None:
            self.analysis = ProfitabilityFinancialAnalysis(self.filtered_data)
            self.calculate_metrics()
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

    def render_sidebar(self):
        st.sidebar.header("Select Charts to Display")
        chart_selection = {
            "Quarter-over-Quarter Revenue Growth":
            st.sidebar.checkbox("Quarter-over-Quarter Revenue Growth",
                                value=True,
                                key="qoq_growth"),
            "Profit Margin Analysis by Quarter":
            st.sidebar.checkbox("Profit Margin Analysis by Quarter",
                                value=False,
                                key="profit_margin"),
            "Expense Ratio Over Time":
            st.sidebar.checkbox("Expense Ratio Over Time",
                                value=False,
                                key="expense_ratio"),
            "Revenue Distribution by Quarter":
            st.sidebar.checkbox("Revenue Distribution by Quarter",
                                value=False,
                                key="revenue_distribution"),
            "Profit Margin Analysis by Quarter (Bar)":
            st.sidebar.checkbox("Profit Margin Analysis by Quarter (Bar)",
                                value=False,
                                key="profit_margin_bar"),
            "Comparative Analysis Over Time":
            st.sidebar.checkbox("Comparative Analysis Over Time",
                                value=False,
                                key="comparative_analysis")
        }
        return chart_selection

    def render_charts(self):
        chart_selection = self.render_sidebar()

        # Ensure at least one chart is selected by default
        if not any(chart_selection.values()):
            chart_selection[
                "Quarter-over-Quarter Revenue Growth"] = True  # Default chart selection

        selected_charts = {
            name: selected
            for name, selected in chart_selection.items() if selected
        }
        tab_names = list(selected_charts.keys())

        # Toggle for showing dynamic insights
        show_dynamic_insights = UIHelpers.switch("Show Dynamic Insights",
                                                 default_value=True,
                                                 in_sidebar=True)

        if show_dynamic_insights:
            main_tab1, main_tab2 = st.tabs(
                ["Financial Overview", "Dynamic Insights"])
        else:
            main_tab1 = st.container()
            st.header("Financial Overview")

        with main_tab1:
            if tab_names:
                tabs = st.tabs(tab_names)

                chart_data_mapping = {
                    "Quarter-over-Quarter Revenue Growth":
                    (self.df_qoq_growth, ),
                    "Profit Margin Analysis by Quarter":
                    (self.df_qoq_growth, ),
                    "Expense Ratio Over Time": (self.df_expense_ratio, ),
                    "Revenue Distribution by Quarter":
                    (self.df_revenue_distribution, ),
                    "Profit Margin Analysis by Quarter (Bar)":
                    (self.df_margin_analysis, ),
                    "Comparative Analysis Over Time": (self.filtered_data, )
                }

                for tab, tab_name in zip(tabs, tab_names):
                    with tab:
                        if tab_name == "Comparative Analysis Over Time":
                            selected_metrics = st.multiselect(
                                'Select metrics for comparative analysis:', [
                                    'NET_INCOME_LOSS', 'OPS_INCOME_LOSS',
                                    'REVENUES'
                                ],
                                default=[
                                    'NET_INCOME_LOSS', 'OPS_INCOME_LOSS',
                                    'REVENUES'
                                ])
                            if selected_metrics:
                                render_chart(tab_name,
                                             *chart_data_mapping[tab_name],
                                             selected_metrics)
                        else:
                            render_chart(tab_name,
                                         *chart_data_mapping[tab_name])

        if show_dynamic_insights:
            with main_tab2:
                self.render_insights(insights_type='dynamic')
