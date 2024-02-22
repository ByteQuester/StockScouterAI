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
        bar_selected_metrics (List[str]): Metrics selected for the bar chart visualization.
        line_filtered_data (json): Filtered data for line chart visualization.
        bar_filtered_data (json): Filtered data for bar chart visualization.
        grid_filtered_data (json): Data prepared for display in a grid format.
    """

    def __init__(self, cik: str):
        super().__init__(cik, "Liquidity")

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
        self.setup_dashboard_button("Liquidity")

        # Initialize dashboard with data if button clicked
        self.initialize_dashboard_with_data(LiquidityDashboardSetup,
                                            self.line_filtered_data,
                                            self.bar_filtered_data,
                                            self.grid_filtered_data)
