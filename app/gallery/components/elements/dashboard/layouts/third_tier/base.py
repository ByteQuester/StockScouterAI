import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import streamlit as st
from streamlit_elements import elements, event, sync

from app.gallery.ui import UIHelpers, update_sidebar
from app.gallery.utils import DataLoader


class DashboardBase(ABC):
    """
    An abstract base class to create and manage the lifecycle of a dynamic dashboard using Streamlit
    and Streamlit Elements. It facilitates data loading, filtering, widget setup, and dashboard rendering.

    Attributes:
        cik (str): Central Index Key to identify the company.
        query_type (str): Type of the query to determine the data processing logic.
        dashboard_initialized (bool): Flag to check if the dashboard should be initialized.
    """

    def __init__(self, cik: str, query_type: str):
        self.ui: UIHelpers = UIHelpers()
        self.data_loader: DataLoader = DataLoader()
        self.cik: str = cik
        self.query_type: str = query_type
        self.dashboard_initialized: bool = False
        self.initialize()

    def initialize_sidebar(self):
        """
        Updates the sidebar with options relevant to the current dashboard.
        This method can be overridden in subclasses if they require a different sidebar setup.
        """
        update_sidebar()

    def setup_dashboard_button(self, dashboard_label: str) -> None:
        """Creates a button to load data for the dashboard."""
        if self.ui.create_button(f'Load {dashboard_label} Data'):
            self.dashboard_initialized = True

    def initialize_dashboard_with_data(self, dashboard_class: Any, *args:
                                       Any) -> None:
        """Initializes the dashboard with provided data if the dashboard has been flagged for initialization."""
        if self.dashboard_initialized:
            formatted_data = [json.dumps(data, indent=2) for data in args]
            st.session_state.dashboard_setup = dashboard_class(*formatted_data)

    @abstractmethod
    def setup_widgets(self) -> None:
        """Abstract method for setting up widgets on the dashboard."""
        pass

    def initialize(self) -> None:
        """Initializes the dashboard by loading data and setting up content."""
        self.select_date_range()
        self.filter_data()
        self.setup_content()
        self.setup_widgets()
        self.initialize_sidebar()

    def select_date_range(self):
        """Allows users to select a date range for data filtering."""
        (start_date, end_date) = self.ui.select_date_range()

        (self.start_date_str,
         self.end_date_str) = (self.ui.format_date(start_date),
                               self.ui.format_date(end_date))

    def filter_data(self) -> None:
        """Filters data based on the selected date range and query type."""
        chart_types = [
            "line_chart", "divergence_chart", "bar_chart", "data_grid"
        ]
        self.initial_filter_data = {
            chart_type:
            self.data_loader.load_and_filter_data(self.cik, self.query_type,
                                                  chart_type,
                                                  self.start_date_str,
                                                  self.end_date_str)
            for chart_type in chart_types
        }

    def get_unique_metrics(self, chart_type: str) -> List[str]:
        """Retrieves unique metrics available for a specific chart type."""
        if chart_type == "bar_chart":
            return self.data_loader.extract_unique_metrics_from_bar_data(
                self.initial_filter_data[chart_type])
        else:
            return [d["id"] for d in self.initial_filter_data[chart_type]
                    ] if self.initial_filter_data[chart_type] else []

    def load_and_filter_grid_data(self) -> Dict[str, Any]:
        """Loads and filters grid chart data based on the selected date range."""
        grid_data = self.data_loader.load_json_data_for_chart(
            self.cik, self.query_type, "data_grid")
        return self.data_loader.filter_grid_by_date(grid_data,
                                                    self.start_date_str,
                                                    self.end_date_str)

    def filter_chart_data(self, chart_type: str,
                          selected_metrics: List[str]) -> Any:
        """Filters chart data based on the selected metrics and chart type."""
        filtered_data = self.data_loader.get_metric_by_selection(
            cik=self.cik,
            query_type=self.query_type,
            chart_type=chart_type,
            selected_metrics=selected_metrics)
        if chart_type == "line_chart" or chart_type == "divergence_chart":
            return self.data_loader.filter_line_by_date(
                filtered_data, self.start_date_str, self.end_date_str)
        elif chart_type == "bar_chart":
            return self.data_loader.filter_bar_by_date(filtered_data,
                                                       self.start_date_str,
                                                       self.end_date_str)
        elif chart_type == "data_grid":
            return self.data_loader.filter_grid_by_date(
                filtered_data, self.start_date_str, self.end_date_str)

    @abstractmethod
    def setup_content(self) -> None:
        """Abstract method to set up dashboard content based on filtered data."""
        pass

    def render_common_widgets(self) -> None:
        """Renders common widgets across all dashboards."""
        if 'dashboard_setup' in st.session_state:
            setup = st.session_state.dashboard_setup
            setup.w.editor()
            if 'Card content' in setup.w.editor._tabs:
                setup.w.card(setup.w.editor.get_content("Card content"))
            if 'Bar chart' in setup.w.editor._tabs:
                setup.w.card(setup.w.editor.get_content("Bar chart"))
            if 'Data grid' in setup.w.editor._tabs:
                setup.w.card(setup.w.editor.get_content("Data grid"))
            if 'Line chart' in setup.w.editor._tabs:
                setup.w.card(setup.w.editor.get_content("Line chart")) #, config_type="base_config")


    def render_dashboard(self) -> None:
        """Renders the dashboard with widgets and content."""
        if 'dashboard_setup' in st.session_state:
            setup = st.session_state.dashboard_setup
            with elements("demo"):
                event.Hotkey("ctrl+s",
                             sync(),
                             bindInputs=True,
                             overrideDefault=True)
                with setup.w.dashboard(rowHeight=57):
                    self.render_common_widgets()
                    # Call a method to render subclass-specific widgets, if any
                    self.render_specific_widgets()

    def render_specific_widgets(self) -> None:
        """Abstract method for rendering dashboard-specific widgets."""
        pass
