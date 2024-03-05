from app.gallery.components.elements.dashboard.setup import \
    AssetsLiabilitiesDashboardSetup

from .base import DashboardBase


class AssetsLiabilitiesDashboard(DashboardBase):
    """
    Inherits from DashboardBase to use its data loading, filtering, and widget setup functionalities.

    Args:
        cik (str): Central Index Key (CIK) number for the company to display data.

    Attributes:
        bar_selected_metrics (List[str]): Selected metrics for the bar chart.
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
        bar_metrics = (self.get_unique_metrics("bar_chart"))

        self.bar_selected_metrics = self.ui.select_metrics(bar_metrics,
                                                           key='bar',
                                                           name='Bar Chart')
        self.bar_filtered_data = self.filter_chart_data(
            "bar_chart", self.bar_selected_metrics)

        # Setup dashboard button
        self.setup_dashboard_button("Assets & Liabilities")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(AssetsLiabilitiesDashboardSetup,
                                            self.bar_filtered_data)
