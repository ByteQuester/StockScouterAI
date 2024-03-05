from app.gallery.components.elements.dashboard.setup import \
    AssetsLiabilitiesDashboardSetup

from .base import DashboardBase


class AssetsLiabilitiesDashboard(DashboardBase):
    """
    Inherits from DashboardBase to use its data loading, filtering, and widget setup functionalities.

    Args:
        cik (str): Central Index Key (CIK) number for the company to display data.

    Attributes:
        grid_filtered_data (Any): Filtered data for the data grid.
    """

    def __init__(self, cik: str):
        super().__init__(cik, "Assets_Liabilities")

    def setup_widgets(self) -> None:
        """Set up widgets specific to the Assets and Liabilities dashboard."""
        pass

    def setup_content(self) -> None:
        """
        Processes data for the dashboard and sets up content based on user-selected metrics
        and filtered data.
        """
        self.grid_filtered_data = self.load_and_filter_grid_data()

        # Setup dashboard button
        self.setup_dashboard_button("Assets & Liabilities")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(AssetsLiabilitiesDashboardSetup,
                                            self.grid_filtered_data)
