# general_dashboard_base.py

import pandas as pd
import streamlit as st

from app.gallery.ui import DynamicInsights, KeyInsights, UIHelpers
from app.gallery.utils.data_loader import DataLoader

from .chart_register import render_chart
from .graph_renderers import *


class GeneralDashboardBase:

    def __init__(self, ciks, query_type):
        self.ciks = ciks
        self.query_type = query_type
        self.data_loader = DataLoader()
        self.data = {
            'Assets_Liabilities': pd.DataFrame(),
            'Cash_Flow': pd.DataFrame(),
            'Profitability': pd.DataFrame(),
            'Liquidity': pd.DataFrame()
        }
        self.load_data()
        self.insights_data = {}
        self.insights_config = []
        self.data_insights = []

    def load_data(self):
        for cik in self.ciks:
            self.data['Assets_Liabilities'] = pd.concat([
                self.data['Assets_Liabilities'],
                self.data_loader.load_csv_data(cik,
                                               query_type='Assets_Liabilities')
            ],
                                                        ignore_index=True)
            self.data['Cash_Flow'] = pd.concat([
                self.data['Cash_Flow'],
                self.data_loader.load_csv_data(cik, query_type='Cash_Flow')
            ],
                                               ignore_index=True)
            self.data['Profitability'] = pd.concat([
                self.data['Profitability'],
                self.data_loader.load_csv_data(cik, query_type='Profitability')
            ],
                                                   ignore_index=True)
            self.data['Liquidity'] = pd.concat([
                self.data['Liquidity'],
                self.data_loader.load_csv_data(cik, query_type='Liquidity')
            ],
                                               ignore_index=True)

    def initialize_analysis(self):
        self.calculate_insights()
        self.configure_insights()

    def calculate_insights(self):
        df_assets_liabilities = self.data['Assets_Liabilities']
        df_cash_flow = self.data['Cash_Flow']
        df_profitability = self.data['Profitability']
        df_liquidity = self.data['Liquidity']

        self.insights_data = {
            'total_assets':
            f"{df_assets_liabilities['ASSETS_CURRENT'].iloc[-1]} mil $",
            'total_liabilities':
            f"{df_assets_liabilities['LIABILITIES_CURRENT'].iloc[-1]} mil $",
            'current_ratio': df_liquidity['CURRENT_RATIO'].iloc[-1],
            'profit_margin': f"{df_profitability['PROFIT_MARGIN'].iloc[-1]}%"
        }

    def configure_insights(self):
        self.insights_config = [{
            'title': 'Total Assets',
            'data_key': 'total_assets'
        }, {
            'title': 'Total Liabilities',
            'data_key': 'total_liabilities'
        }, {
            'title': 'Current Ratio',
            'data_key': 'current_ratio',
            'format': '{value:.2f}'
        }, {
            'title': 'Profit Margin',
            'data_key': 'profit_margin'
        }]

        self.data_insights = [
            {
                'label':
                'Profit Margin Trend',
                'calculation':
                lambda: "increasing" if self.data['Profitability'][
                    'PROFIT_MARGIN'].iloc[-1] > self.data['Profitability'][
                        'PROFIT_MARGIN'].iloc[0] else "decreasing",
                'positive_outcomes': ['increasing'],
                'explanation':
                'An increasing trend suggests that the company is becoming more efficient in converting sales into actual profit, indicating financial health.'
            },
            {
                'label':
                'Cash Flow Health',
                'calculation':
                lambda: "healthy" if self.data['Cash_Flow'][
                    'CASH_FLOW_OPERATING'].iloc[-1] > 0 else "concerning",
                'positive_outcomes': ['healthy'],
                'explanation':
                'Positive cash flow from operations signifies a company solid financial position, ensuring it can meet its obligations and invest in growth.'
            },
            {
                'label':
                'Liquidity Position',
                'calculation':
                lambda: "good" if self.data['Liquidity']['CURRENT_RATIO'].iloc[
                    -1] > 1 else "poor",
                'positive_outcomes': ['good'],
                'explanation':
                'A current ratio above 1 indicates that the company has more current assets than current liabilities, suggesting good short-term financial stability.'
            },
            {
                'label':
                'Leverage Situation',
                'calculation':
                lambda: "increasing risk"
                if self.data['Assets_Liabilities']['DEBT_TO_EQUITY_RATIO'].
                iloc[-1] > self.data['Assets_Liabilities'][
                    'DEBT_TO_EQUITY_RATIO'].iloc[0] else "stable",
                'positive_outcomes': ['stable'],
                'explanation':
                'A stable or low debt-to-equity ratio indicates that the company is not overly reliant on debt financing, reducing financial risk.'
            },
        ]

    def render_sidebar(self):
        st.sidebar.header("Select Charts to Display")
        chart_selection = {
            "Assets vs Liabilities":
            st.sidebar.checkbox("Assets vs Liabilities",
                                value=True,
                                key="assets_vs_liabilities"),
            "Debt to Equity Ratio":
            st.sidebar.checkbox("Debt to Equity Ratio",
                                value=False,
                                key="debt_to_equity_ratio"),
            "Cash Flow Summary":
            st.sidebar.checkbox("Cash Flow Summary",
                                value=False,
                                key="cash_flow_summary"),
            "Profit Margin Trend":
            st.sidebar.checkbox("Profit Margin Trend",
                                value=False,
                                key="profit_margin_trend"),
            "Current Ratio Trend":
            st.sidebar.checkbox("Current Ratio Trend",
                                value=False,
                                key="current_ratio_trend")
        }
        return chart_selection

    def render_tabs(self, chart_selection, view_type):
        if not any(chart_selection.values()):
            chart_selection[next(iter(chart_selection))] = True

        selected_charts = {
            name: selected
            for name, selected in chart_selection.items() if selected
        }
        tab_names = list(selected_charts.keys())

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
                    "Assets vs Liabilities":
                    (self.data['Assets_Liabilities'], view_type),
                    "Debt to Equity Ratio":
                    (self.data['Assets_Liabilities'], view_type),
                    "Cash Flow Summary": (self.data['Cash_Flow'], view_type),
                    "Profit Margin Trend":
                    (self.data['Profitability'], view_type),
                    "Current Ratio Trend": (self.data['Liquidity'], view_type)
                }

                for tab, tab_name in zip(tabs, tab_names):
                    with tab:
                        render_chart(tab_name, *chart_data_mapping[tab_name])

        if show_dynamic_insights:
            with main_tab2:
                self.render_insights()

    def render_insights(self):
        st.header('Key Financial Insights')
        st.divider()
        key_insights = KeyInsights(self.insights_data, self.insights_config)
        key_insights.render()
        st.divider()

        st.subheader("Observations")
        st.success(
            "The Observations are purely educational and for academic purposes. No one is advised on taking financial decisions off these data points solely."
        )
        for insight in self.data_insights:
            dynamic_insights = DynamicInsights([insight])
            dynamic_insights.render()
            st.markdown("---")
