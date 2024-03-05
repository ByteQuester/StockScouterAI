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
        bar_selected_metrics (List[str]): Metrics selected by the user for bar chart visualization.
        bar_filtered_data (Any): Data filtered for bar chart based on selected metrics.
    """

    def __init__(self, cik: str):
        super().__init__(cik, "Cash_Flow")

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
        self.setup_dashboard_button("Cash Flow")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(CashFlowDashboardSetup,
                                            self.bar_filtered_data)