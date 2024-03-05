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
        bar_selected_metrics (List[str]): Metrics selected for the bar chart visualization.
        bar_filtered_data (json): Filtered data for bar chart visualization.
    """

    def __init__(self, cik: str):
        super().__init__(cik, "Profitability")

    def setup_widgets(self) -> None:
        # Setup widgets specific to Profitability dashboard
        pass

    def setup_content(self) -> None:
        # Data processing
        bar_metrics = (self.get_unique_metrics("bar_chart"))

        self.bar_selected_metrics = self.ui.select_metrics(bar_metrics,
                                                           key='bar',
                                                           name='Bar Chart')

        self.bar_filtered_data = self.filter_chart_data(
            "bar_chart", self.bar_selected_metrics)

        # Setup dashboard button
        self.setup_dashboard_button("Profitability")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(ProfitabilityDashboardSetup,
                                            self.bar_filtered_data)
