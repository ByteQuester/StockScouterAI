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
        bar_selected_metrics (List[str]): Metrics selected by the user for bar chart visualization.
        line_filtered_data (Any): Data filtered for line chart based on selected metrics.
        bar_filtered_data (Any): Data filtered for bar chart based on selected metrics.
        grid_filtered_data (Any): Data filtered for grid display.
    """
    def __init__(self, cik: str):
        super().__init__(cik, "Cash_Flow")

    def setup_widgets(self) -> None:
        # Setup widgets specific to Profitability dashboard
        pass

    def setup_content(self) -> None:
        # Data processing
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
        self.setup_dashboard_button("Cash Flow")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(CashFlowDashboardSetup,
                                            self.line_filtered_data,
                                            self.bar_filtered_data,
                                            self.grid_filtered_data)
