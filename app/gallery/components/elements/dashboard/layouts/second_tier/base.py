import pandas as pd
import streamlit as st

from app.gallery.ui import UIHelpers, update_sidebar
from app.gallery.ui.insight_keys import KeyInsights
from app.gallery.ui.take_aways import DynamicInsights
from app.gallery.utils import DataLoader


class SecondTierViewBase:

    def __init__(self, ciks, query_type):
        self.ciks = ciks
        self.query_type = query_type
        self.ui: UIHelpers = UIHelpers()
        self.data_loader: DataLoader = DataLoader()
        self.data = None  # Initialize self.data here
        self.filtered_data = None  # Initialize self.filtered_data here
        self.insights_data = {}
        self.insights_config = []
        self.data_insights = []
        self.initialize_sidebar()

    def initialize_sidebar(self):
        """
        Updates the sidebar with options relevant to the current dashboard.
        This method can be overridden in subclasses if they require a different sidebar setup.
        """
        update_sidebar()

    def load_data(self):
        """Load and preprocess data."""
        self.data = self.data_loader.load_data_for_ciks(self.ciks,
                                                   query_type=self.query_type)
        self.data['DATE'] = pd.to_datetime(self.data['DATE'])

    def define_range(self):
        """Define the min and max date range."""
        if self.data is not None:
            min_date, max_date = self.data['DATE'].dt.date.min(
            ), self.data['DATE'].dt.date.max()
            return min_date, max_date
        else:
            return None, None  # Return None if self.data is not loaded

    def select_date_range(self):
        """Select date range using UIHelpers."""
        min_date, max_date = self.define_range(
        )  # Call define_range to get min and max date
        if min_date is not None and max_date is not None:
            start_date, end_date = self.ui.select_date_slider(
                min_date, max_date)
            if start_date and end_date:
                return start_date, end_date
            else:
                st.error("Please select a valid date range.")
                return None, None
        else:
            st.error("Data not loaded or no date range was selected.")
            return None, None

    def filter_data_by_date(self, min_date, max_date):
        """Filter data by date range."""
        if self.data is not None:
            self.filtered_data = self.data[
                (self.data['DATE'] >= pd.to_datetime(min_date))
                & (self.data['DATE'] <= pd.to_datetime(max_date))]
        else:
            self.filtered_data = None

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
