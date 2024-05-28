import streamlit as st

from app.gallery.components.elements.dashboard.setup import render_chart
from app.gallery.ui import UIHelpers
from app.services.queries.dev_tables import CashFlowAnalysis

from ..base import SecondTierViewBase
from .graph_renderers import *


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

    def render_sidebar(self):
        st.sidebar.header("Select Charts to Display")
        chart_selection = {
            "Year-over-Year Cash Flow Growth":
            st.sidebar.checkbox("Year-over-Year Cash Flow Growth",
                                value=True,
                                key="cash_flow_yoy_growth"),
            "Net Cash Flow Over Time":
            st.sidebar.checkbox("Net Cash Flow Over Time",
                                value=False,
                                key="net_cash_flow"),
            "Comparative Analysis Over Time":
            st.sidebar.checkbox("Comparative Analysis Over Time",
                                value=False,
                                key="comparative_analysis_cash_flow")
        }
        return chart_selection

    def render_charts(self):
        chart_selection = self.render_sidebar()

        # Ensure at least one chart is selected by default
        if not any(chart_selection.values()):
            chart_selection[
                "Year-over-Year Cash Flow Growth"] = True  # Default chart selection

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
                ["Cash Flow Overview", "Dynamic Insights"])
        else:
            main_tab1 = st.container()
            st.header("Cash Flow Overview")

        with main_tab1:
            if tab_names:
                tabs = st.tabs(tab_names)

                chart_data_mapping = {
                    "Year-over-Year Cash Flow Growth": (self.df_yoy_growth, ),
                    "Net Cash Flow Over Time": (self.df_net_flow, ),
                    "Comparative Analysis Over Time": (self.filtered_data, )
                }

                for tab, tab_name in zip(tabs, tab_names):
                    with tab:
                        if tab_name == "Year-over-Year Cash Flow Growth":
                            for column in [
                                    'CASH_FLOW_FINANCING_YoY',
                                    'CASH_FLOW_INVESTING_YoY',
                                    'CASH_FLOW_OPERATING_YoY'
                            ]:
                                if column in self.df_yoy_growth.columns:
                                    render_chart(tab_name, self.df_yoy_growth,
                                                 column)
                        elif tab_name == "Comparative Analysis Over Time":
                            selected_metrics = st.multiselect(
                                'Select metrics for comparative analysis:', [
                                    'CASH_FLOW_FINANCING',
                                    'CASH_FLOW_INVESTING',
                                    'CASH_FLOW_OPERATING'
                                ],
                                default=[
                                    'CASH_FLOW_FINANCING',
                                    'CASH_FLOW_INVESTING',
                                    'CASH_FLOW_OPERATING'
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
