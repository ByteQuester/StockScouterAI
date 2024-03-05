from app.gallery.components.elements.dashboard.setup import \
    LiquidityDashboardSetup

from .base import DashboardBase


class LiquidityDashboard(DashboardBase):
    """
    A dashboard class specialized in visualizing liquidity data, extending the generic DashboardBase.

    This class handles the setup of widgets specific to liquidity data visualization and processes
    data to be displayed based on user-selected metrics.

    Args:
        cik (str): The Central Index Key (CIK) number identifying the company of interest.

    Attributes:
        line_selected_metrics (List[str]): Metrics selected for the line chart visualization.
        line_filtered_data (json): Filtered data for line chart visualization.
    """

    def __init__(self, cik: str):
        super().__init__(cik, "Liquidity")

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
        self.setup_dashboard_button("Liquidity")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(LiquidityDashboardSetup,
                                            self.line_filtered_data)
