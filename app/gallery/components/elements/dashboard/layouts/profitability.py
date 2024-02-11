import streamlit as st

from app.gallery.components.elements.dashboard.setup import \
    ProfitabilityDashboardSetup

from .base import DashboardBase


class ProfitabilityDashboard(DashboardBase):
    """
    A dashboard class specialized in visualizing profitability data, extending the generic DashboardBase.

    This class handles the setup of widgets specific to profitability data visualization and processes
    data to be displayed based on user-selected metrics.

    Args:
        cik (str): The Central Index Key (CIK) number identifying the company of interest.

    Attributes:
        line_selected_metrics (List[str]): Metrics selected for the line chart visualization.
        bar_selected_metrics (List[str]): Metrics selected for the bar chart visualization.
        divergence_selected_metrics (List[str]): Metrics selected for the divergence chart visualization.
        line_filtered_data (json): Filtered data for line chart visualization.
        bar_filtered_data (json): Filtered data for bar chart visualization.
        divergence_filtered_data (json): Filtered data for divergence chart visualization.
        grid_filtered_data (json): Data prepared for display in a grid format.
    """

    def __init__(self, cik: str):
        super().__init__(cik, "Profitability")

    def setup_widgets(self) -> None:
        # Setup widgets specific to Profitability dashboard
        pass

    def setup_content(self) -> None:
        # Data processing
        line_metrics = (self.get_unique_metrics("line_chart"))
        bar_metrics = (self.get_unique_metrics("bar_chart"))
        divergence_metrics = (self.get_unique_metrics("divergence_chart"))

        self.line_selected_metrics = self.ui.select_metrics(line_metrics,
                                                            key='line',
                                                            name='Line Chart')
        self.bar_selected_metrics = self.ui.select_metrics(bar_metrics,
                                                           key='bar',
                                                           name='Bar Chart')
        self.divergence_selected_metrics = self.ui.select_metrics(
            divergence_metrics, key='divergence', name='Divergence Chart')

        self.line_filtered_data = self.filter_chart_data(
            "line_chart", self.line_selected_metrics)
        self.bar_filtered_data = self.filter_chart_data(
            "bar_chart", self.bar_selected_metrics)
        self.divergence_filtered_data = self.filter_chart_data(
            "divergence_chart", self.divergence_selected_metrics)
        self.grid_filtered_data = self.load_and_filter_grid_data()

        # Setup dashboard button
        self.setup_dashboard_button("Profitability")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(ProfitabilityDashboardSetup,
                                            self.line_filtered_data,
                                            self.divergence_filtered_data,
                                            self.bar_filtered_data,
                                            self.grid_filtered_data)

    def render_specific_widgets(self) -> None:
        """
        Renders widgets specific to the Profitability dashboard. This method can be overridden
        in subclasses to provide custom widget setups for specific types of dashboards.
        """
        if 'dashboard_setup' in st.session_state:
            setup = st.session_state.dashboard_setup
            # Addressing session.state issue #1:
            # Check if the divergence_line widget is defined before attempting to render it
            # Prevents AttributeError: 'types.SimpleNamespace' object
            if hasattr(setup.w, 'divergence_line'):
                setup.w.divergence_line(
                    setup.w.editor.get_content("Divergence chart"),
                    config_type="divergence_chart_config")
