from app.gallery.components.elements.dashboard.setup import \
    CashFlowDashboardSetup

from .base import DashboardBase


class CashFlowDashboard(DashboardBase):
    """
    Dashboard for displaying Cash Flow data, extending the DashboardBase with specific
    functionalities for Cash Flow visualization.

    Args:
        cik (str): The Central Index Key (CIK) number for the company whose data is displayed.

    Attributes:
        grid_filtered_data (Any): Data filtered for grid display.
    """

    def __init__(self, cik: str):
        super().__init__(cik, "Cash_Flow")

    def setup_widgets(self) -> None:
        # Setup widgets specific to Profitability dashboard
        pass

    def setup_content(self) -> None:
        # Data processing
        self.grid_filtered_data = self.load_and_filter_grid_data()

        # Setup dashboard button
        self.setup_dashboard_button("Cash Flow")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(CashFlowDashboardSetup,
                                            self.grid_filtered_data)
