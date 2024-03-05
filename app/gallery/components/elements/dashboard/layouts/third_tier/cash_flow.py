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
        line_selected_metrics (List[str]): Metrics selected by the user for line chart visualization.
        line_filtered_data (Any): Data filtered for line chart based on selected metrics.
    """

    def __init__(self, cik: str):
        super().__init__(cik, "Cash_Flow")

    def setup_widgets(self) -> None:
        # Setup widgets specific to Profitability dashboard
        pass

    def setup_content(self) -> None:
        # Data processing
        line_metrics = (self.get_unique_metrics("line_chart"))

        self.line_selected_metrics = self.ui.select_metrics(line_metrics,
                                                            key='line',
                                                            name='Line Chart')

        self.line_filtered_data = self.filter_chart_data(
            "line_chart", self.line_selected_metrics)

        # Setup dashboard button
        self.setup_dashboard_button("Cash Flow")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(CashFlowDashboardSetup,
                                            self.line_filtered_data)
