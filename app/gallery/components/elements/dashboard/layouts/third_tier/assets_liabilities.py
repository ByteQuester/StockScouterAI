from app.gallery.components.elements.dashboard.setup import \
    AssetsLiabilitiesDashboardSetup

from .base import DashboardBase


class AssetsLiabilitiesDashboard(DashboardBase):
    """
    Inherits from DashboardBase to use its data loading, filtering, and widget setup functionalities.

    Args:
        cik (str): Central Index Key (CIK) number for the company to display data.

    Attributes:
        line_selected_metrics (List[str]): Selected metrics for the line chart.
        line_filtered_data (Any): Filtered data for the line chart based on selected metrics.
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
        line_metrics = (self.get_unique_metrics("line_chart"))

        self.line_selected_metrics = self.ui.select_metrics(line_metrics,
                                                            key='line',
                                                            name='Line Chart')

        self.line_filtered_data = self.filter_chart_data(
            "line_chart", self.line_selected_metrics)

        # Setup dashboard button
        self.setup_dashboard_button("Assets & Liabilities")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(AssetsLiabilitiesDashboardSetup,
                                            self.line_filtered_data)
