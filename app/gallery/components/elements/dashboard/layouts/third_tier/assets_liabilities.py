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
        bar_selected_metrics (List[str]): Selected metrics for the bar chart.
        line_filtered_data (Any): Filtered data for the line chart based on selected metrics.
        bar_filtered_data (Any): Filtered data for the bar chart based on selected metrics.
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
        line_metrics = (self.get_unique_metrics("line_chart"))
        bar_metrics = (self.get_unique_metrics("bar_chart"))

        self.line_selected_metrics = self.ui.select_metrics(line_metrics,
                                                            key='line',
                                                            name='Line Chart')
        self.bar_selected_metrics = self.ui.select_metrics(bar_metrics,
                                                           key='bar',
                                                           name='Bar Chart')

        self.line_filtered_data = self.filter_chart_data(
            "line_chart", self.line_selected_metrics)
        self.bar_filtered_data = self.filter_chart_data(
            "bar_chart", self.bar_selected_metrics)
        self.grid_filtered_data = self.load_and_filter_grid_data()

        # Setup dashboard button
        self.setup_dashboard_button("Assets & Liabilities")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(AssetsLiabilitiesDashboardSetup,
                                            self.line_filtered_data,
                                            self.bar_filtered_data,
                                            self.grid_filtered_data)
