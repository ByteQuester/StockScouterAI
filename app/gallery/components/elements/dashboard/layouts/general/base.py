# general.base.py(dev)

import pandas as pd
import streamlit as st

from app.gallery.ui import UIHelpers, update_sidebar
from app.gallery.ui.insight_keys import KeyInsights
from app.gallery.ui.take_aways import DynamicInsights
from app.gallery.utils import DataLoader


class GeneralViewBase:

    def __init__(self, ciks, query_type):
        self.ciks = ciks
        self.query_type = query_type
        self.ui: UIHelpers = UIHelpers()
        self.data_loader: DataLoader = DataLoader()
        self.data = {
            'Assets_Liabilities': pd.DataFrame(),
            'Cash_Flow': pd.DataFrame(),
            'Profitability': pd.DataFrame(),
            'Liquidity': pd.DataFrame()
        }
        self.filtered_data = {
            'Assets_Liabilities': pd.DataFrame(),
            'Cash_Flow': pd.DataFrame(),
            'Profitability': pd.DataFrame(),
            'Liquidity': pd.DataFrame()
        }
        self.insights_data = {}
        self.insights_config = []
        self.data_insights = []

    def load_data(self):
        """Load and preprocess data for each CIK and query type."""
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

        for key in self.data:
            self.data[key]['DATE'] = pd.to_datetime(self.data[key]['DATE'])
            self.filtered_data[key] = self.data[
                key]  # Directly assigning the data to filtered_data

    def calculate_metrics(self):
        """Calculate specific financial metrics. To be implemented by subclasses."""
        raise NotImplementedError

    def generate_insights(self):
        """Generate insights based on calculated metrics. To be implemented by subclasses."""
        raise NotImplementedError

    def render_charts(self):
        """Render charts for visualization. To be implemented by subclasses."""
        raise NotImplementedError

    def render_insights(self, insights_type='all'):
        """Render insights for visualization."""
        if insights_type in ['all', 'key'] and hasattr(
                self, 'insights_data') and hasattr(self, 'insights_config'):
            key_insights = KeyInsights(self.insights_data,
                                       self.insights_config)
            key_insights.render()

        if insights_type in ['all', 'dynamic'] and hasattr(
                self, 'data_insights'):
            dynamic_insights = DynamicInsights(self.data_insights)
            dynamic_insights.render()
