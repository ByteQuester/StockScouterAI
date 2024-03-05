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
        grid_filtered_data (json): Data prepared for display in a grid format.
    """

    def __init__(self, cik: str):
        super().__init__(cik, "Profitability")

    def setup_widgets(self) -> None:
        # Setup widgets specific to Profitability dashboard
        pass

    def setup_content(self) -> None:
        self.grid_filtered_data = self.load_and_filter_grid_data()

        # Setup dashboard button
        self.setup_dashboard_button("Profitability")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(ProfitabilityDashboardSetup,
                                            self.grid_filtered_data)
