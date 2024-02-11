import pandas as pd
import streamlit as st


class UIHelpers:

    @staticmethod
    def create_button(label):
        """Creates a button with a given label."""
        return st.button(label)

    @staticmethod
    def select_date_range(default_start="1Y"):
        """Allows selection of a date range without creating a button."""
        today = pd.to_datetime("today")
        date_ranges = {
            "1Y": today - pd.DateOffset(years=1),
            "5Y": today - pd.DateOffset(years=5),
            "10Y": today - pd.DateOffset(years=10),
        }
        selected_range_key = st.radio("Select Date Range",
                                      list(date_ranges.keys()),
                                      horizontal=True)
        start_date = date_ranges[selected_range_key]
        end_date = today  # Assuming end date is always today for simplicity
        return start_date, end_date

    @staticmethod
    def format_date(date):
        """Formats a datetime object to a string."""
        return date.strftime("%Y-%m")

    @staticmethod
    def select_metrics(unique_metrics, key=None, name=None):
        """Creates a multi-select widget for selecting metrics."""
        return st.multiselect(f'Select {name} metrics to display',
                              unique_metrics,
                              default=unique_metrics,
                              key=key)
