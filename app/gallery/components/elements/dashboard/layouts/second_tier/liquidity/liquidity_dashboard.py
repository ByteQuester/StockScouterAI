import streamlit as st

from app.gallery.components.elements.dashboard.setup import render_chart
from app.gallery.ui import UIHelpers
from app.services.queries.dev_tables import LiquidityAnalysis

from ..base import SecondTierViewBase
from .garph_renderers import *


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

    def render_sidebar(self):
        st.sidebar.header("Select Charts to Display")
        chart_selection = {
            "Quarter-over-Quarter Growth of Current Assets":
            st.sidebar.checkbox(
                "Quarter-over-Quarter Growth of Current Assets",
                value=True,
                key="liquidity_qoq_growth"),
            "Current Ratio Over Time":
            st.sidebar.checkbox("Current Ratio Over Time",
                                value=False,
                                key="current_ratio"),
            "Comparative Analysis Over Time":
            st.sidebar.checkbox("Comparative Analysis Over Time",
                                value=False,
                                key="comparative_analysis_liquidity")
        }
        return chart_selection

    def render_charts(self):
        chart_selection = self.render_sidebar()

        # Ensure at least one chart is selected by default
        if not any(chart_selection.values()):
            chart_selection[
                "Quarter-over-Quarter Growth of Current Assets"] = True  # Default chart selection

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
                ["Liquidity Overview", "Dynamic Insights"])
        else:
            main_tab1 = st.container()
            st.header("Liquidity Overview")

        with main_tab1:
            if tab_names:
                tabs = st.tabs(tab_names)

                chart_data_mapping = {
                    "Quarter-over-Quarter Growth of Current Assets":
                    (self.df_qoq_growth, ),
                    "Current Ratio Over Time": (self.filtered_data, ),
                    "Comparative Analysis Over Time": (self.filtered_data, )
                }

                for tab, tab_name in zip(tabs, tab_names):
                    with tab:
                        if tab_name == "Comparative Analysis Over Time":
                            selected_metrics = st.multiselect(
                                'Select metrics for comparative analysis:',
                                ['CURRENT_ASSETS', 'CURRENT_LIABILITIES'],
                                default=[
                                    'CURRENT_ASSETS', 'CURRENT_LIABILITIES'
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
