import streamlit as st

from app.gallery.ui import UIHelpers
from app.services.queries.dev_tables import AssetsLiabilitiesEquityAnalysis

from ..base import SecondTierViewBase
from ..chart_registry import render_chart
from .graph_renderers import *


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

    def render_sidebar(self):
        st.sidebar.header("Select Charts to Display")
        chart_selection = {
            "Quarter-over-Quarter Growth of Current Assets":
            st.sidebar.checkbox(
                "Quarter-over-Quarter Growth of Current Assets",
                value=True,
                key="assets_qoq_growth"),
            "Working Capital Over Time":
            st.sidebar.checkbox("Working Capital Over Time",
                                value=False,
                                key="working_capital"),
            "Asset To Liability Ratio Over Time":
            st.sidebar.checkbox("Asset To Liability Ratio Over Time",
                                value=False,
                                key="asset_liability_ratio"),
            "Debt to Equity Ratio Over Time":
            st.sidebar.checkbox("Debt to Equity Ratio Over Time",
                                value=False,
                                key="debt_equity_ratio"),
            "Comparative Analysis Over Time":
            st.sidebar.checkbox("Comparative Analysis Over Time",
                                value=False,
                                key="comparative_analysis_assets")
        }
        return chart_selection

    def render_charts(self):
        chart_selection = self.render_sidebar()

        # Ensure at least one chart is selected by default
        if not any(chart_selection.values()):
            chart_selection[next(iter(
                chart_selection))] = True  # Selects the first chart by default

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
            # Create both tabs if dynamic insights are to be shown
            main_tab1, main_tab2 = st.tabs(
                ["Financial Overview", "Dynamic Insights"])
        else:
            # Only create the Financial Overview tab if dynamic insights are not to be shown
            main_tab1 = st.container()
            st.header("Financial Overview")

        with main_tab1:
            if tab_names:
                tabs = st.tabs(tab_names)

                chart_data_mapping = {
                    "Quarter-over-Quarter Growth of Current Assets":
                    (self.df_qoq_growth, ),
                    "Working Capital Over Time": (self.df_working_capital, ),
                    "Asset To Liability Ratio Over Time":
                    (self.filtered_data, ),
                    "Debt to Equity Ratio Over Time": (self.filtered_data, ),
                    "Comparative Analysis Over Time": (self.filtered_data, )
                }

                for tab, tab_name in zip(tabs, tab_names):
                    with tab:
                        if tab_name == "Comparative Analysis Over Time":
                            selected_metrics = st.multiselect(
                                'Select metrics for comparative analysis:', [
                                    'ASSETS_CURRENT', 'LIABILITIES_CURRENT',
                                    'STOCKHOLDERS_EQUITY'
                                ],
                                default=[
                                    'ASSETS_CURRENT', 'LIABILITIES_CURRENT'
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
