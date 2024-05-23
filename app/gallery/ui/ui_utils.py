import pandas as pd
import streamlit as st


class UIHelpers:

    @staticmethod
    def create_button(label, in_sidebar=False):
        """Creates a button with a given label."""
        if in_sidebar:
            return st.sidebar.button(label)
        return st.button(label)

    @staticmethod
    def select_date_range(default_start="1Y", in_sidebar=False):
        """Allows selection of a date range without creating a button."""
        today = pd.to_datetime("today")
        date_ranges = {
            "1Y": today - pd.DateOffset(years=1),
            "5Y": today - pd.DateOffset(years=5),
            "10Y": today - pd.DateOffset(years=10),
        }
        location = st.sidebar if in_sidebar else st
        selected_range_key = location.radio("Select Date Range",
                                            list(date_ranges.keys()),
                                            horizontal=True)
        start_date = date_ranges[selected_range_key]
        end_date = today  # Assuming end date is always today for simplicity
        return start_date, end_date

    @staticmethod
    def select_date_slider(min_date,
                           max_date,
                           default_range=None,
                           in_sidebar=False):
        """Creates a date slider for selecting a date range.

        :param min_date: The minimum date available for selection.
        :param max_date: The maximum date available for selection.
        :param default_range: A tuple (start_date, end_date) as default values.
        :param in_sidebar: Boolean to determine if the slider should be in the sidebar.
        :return: A tuple (start_date, end_date) representing the selected date range.
        """
        location = st.sidebar if in_sidebar else st
        start_date, end_date = location.slider("Select Date Range",
                                               min_value=min_date,
                                               max_value=max_date,
                                               value=default_range
                                               or (min_date, max_date))
        return start_date, end_date

    @staticmethod
    def switch(label, default_value=False, in_sidebar=False):
        """Creates a switch with a given label."""
        location = st.sidebar if in_sidebar else st
        return location.checkbox(label, value=default_value)
