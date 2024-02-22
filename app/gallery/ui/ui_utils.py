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
    def select_date_slider(min_date, max_date, default_range=None):
        """Creates a date slider for selecting a date range.

        :param min_date: The minimum date available for selection.
        :param max_date: The maximum date available for selection.
        :param default_range: A tuple (start_date, end_date) as default values.
        :return: A tuple (start_date, end_date) representing the selected date range.
        """
        if not min_date or not max_date or min_date > max_date:
            st.error("Invalid date range provided.")
            return None, None

        if default_range is None:
            default_range = (min_date, max_date)

        start_date, end_date = st.slider("Select Date Range",
                                         min_value=min_date,
                                         max_value=max_date,
                                         value=default_range,
                                         format="YYYY-MM")
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
