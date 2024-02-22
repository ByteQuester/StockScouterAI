import json
from abc import ABC, abstractmethod
from types import SimpleNamespace

from app.gallery.components.elements.charts import (Bar, Card, Dashboard,
                                                    DataGrid, Editor, Line)
from app.gallery.components.elements.dashboard.types import *


class DashboardSetup(ABC):
    """
    Abstract base class to set up a dashboard layout with widgets. This class initializes a dashboard and allows
    for the setup of various widgets like editors, line charts, cards, etc., which can be extended by subclasses to
    create specific dashboard configurations.

    Attributes:
        board (Dashboard): The dashboard instance where widgets are added.
        w (SimpleNamespace): A namespace for easy access to initialized widgets.
    """

    def __init__(self):
        self.board = None
        self.w = None
        self.setup_board()
        self.setup_widgets()

    def initialize(self):
        # This method now explicitly calls setup_content, to be called after subclass initialization
        self.setup_content()

    def setup_board(self):
        # Initialize the dashboard here
        self.board = Dashboard()

    def setup_widgets(self):
        # This method sets up widgets and can be overridden by subclasses for custom setups
        self.w = SimpleNamespace(
            dashboard=self.board,
            editor=Editor(self.board, 0, 2, 6, 4, minW=3, minH=5),
            line=Line(self.board, 0, 6, 6, 4, minW=2, minH=4),
            card=Card(self.board, 0, 0, 12, 3, minW=2, minH=4),
        )

    @abstractmethod
    def setup_content(self):
        pass


class InitialDashboardSetup(DashboardSetup):

    def __init__(self):
        super().__init__()
        self.initialize()

    def setup_content(self):
        # Initial content setup specific to the initial dashboard
        self.w.editor.add_tab("Card content", Card.DEFAULT_CONTENT,
                              "plaintext")
        self.w.editor.add_tab("Line chart",
                              json.dumps(Line.DEFAULT_DATA, indent=2), "json")


class ProfitabilityDashboardSetup(DashboardSetup):

    def __init__(self,
                 line_data=None,
                 divergence_line_data=None,
                 bar_data=None,
                 grid_data=None):
        self.card_content = PROFITABILITY_CARD_CONTENT
        self.line_data = line_data
        self.divergence_line_data = divergence_line_data
        self.bar_data = bar_data
        self.grid_data = grid_data
        super().__init__()
        self.initialize()

    def setup_widgets(self):
        super().setup_widgets()
        self.w.divergence_line = Line(self.board, 6, 2, 6, 4, minH=5)
        self.w.bar_chart = Bar(self.board,
                               6,
                               6,
                               6,
                               4,
                               minH=5,
                               keys=[
                                   "NET_INCOME_LOSSValue", "REVENUESValue",
                                   "OPS_INCOME_LOSSValue"
                               ])
        self.w.grid_chart = DataGrid(self.board,
                                     0,
                                     10,
                                     12,
                                     4,
                                     minH=4,
                                     columns=PROFITABILITY_DEFAULT_COLUMNS)

    def setup_content(self):
        # Update content based on some conditions like button press
        self.w.editor.add_tab("Card content", self.card_content, "plaintext")
        self.w.editor.add_tab("Line chart", self.line_data, "json")
        self.w.editor.add_tab("Divergence chart", self.divergence_line_data,
                              "json")
        self.w.editor.add_tab("Bar chart", self.bar_data, "json")
        self.w.editor.add_tab("Data grid", self.grid_data, "json")


class AssetsLiabilitiesDashboardSetup(DashboardSetup):

    def __init__(self, line_data, bar_data, grid_data):
        self.card_content = ASSETS_LIABILITIES_CARD_CONTENT
        self.line_data = line_data
        self.bar_data = bar_data
        self.grid_data = grid_data
        super().__init__()
        self.initialize()

    def setup_widgets(self):
        super().setup_widgets()
        self.w.bar_chart = Bar(self.board,
                               6,
                               6,
                               6,
                               4,
                               minH=5,
                               keys=[
                                   "ASSETS_CURRENTValue",
                                   "LIABILITIES_CURRENTValue",
                                   "STOCKHOLDERS_EQUITYValue"
                               ])
        self.w.grid_chart = DataGrid(
            self.board,
            0,
            10,
            12,
            4,
            minH=4,
            columns=ASSETS_LIABILITIES_DEFAULT_COLUMNS)

    def setup_content(self):
        self.w.editor.add_tab("Card content", self.card_content, "plaintext")
        self.w.editor.add_tab("Line chart", self.line_data, "json")
        self.w.editor.add_tab("Bar chart", self.bar_data, "json")
        self.w.editor.add_tab("Data grid", self.grid_data, "json")


class CashFlowDashboardSetup(DashboardSetup):

    def __init__(self, line_data, bar_data, grid_data):
        self.card_content = CASH_FLOW_CARD_CONTENT
        self.line_data = line_data
        self.bar_data = bar_data
        self.grid_data = grid_data
        super().__init__()
        self.initialize()

    def setup_widgets(self):
        super().setup_widgets()
        self.w.bar_chart = Bar(self.board,
                               6,
                               6,
                               6,
                               4,
                               minH=5,
                               keys=[
                                   "CASH_FLOW_FINANCINGValue",
                                   "CASH_FLOW_INVESTINGValue",
                                   "CASH_FLOW_OPERATINGValue"
                               ])
        self.w.grid_chart = DataGrid(self.board,
                                     0,
                                     10,
                                     12,
                                     4,
                                     minH=4,
                                     columns=CASH_FLOW_DEFAULT_COLUMNS)

    def setup_content(self):
        self.w.editor.add_tab("Card content", self.card_content, "plaintext")
        self.w.editor.add_tab("Line chart", self.line_data, "json")
        self.w.editor.add_tab("Bar chart", self.bar_data, "json")
        self.w.editor.add_tab("Data grid", self.grid_data, "json")


class LiquidityDashboardSetup(DashboardSetup):

    def __init__(self, line_data, bar_data, grid_data):
        self.card_content = LIQUIDITY_CARD_CONTENT
        self.line_data = line_data
        self.bar_data = bar_data
        self.grid_data = grid_data
        super().__init__()
        self.initialize()

    def setup_widgets(self):
        super().setup_widgets()
        self.w.bar_chart = Bar(
            self.board,
            6,
            6,
            6,
            4,
            minH=5,
            keys=["CURRENT_ASSETSValue", "CURRENT_LIABILITIESValue"])
        self.w.grid_chart = DataGrid(self.board,
                                     0,
                                     10,
                                     12,
                                     4,
                                     minH=4,
                                     columns=LIQUIDITY_DEFAULT_COLUMNS)

    def setup_content(self):
        self.w.editor.add_tab("Card content", self.card_content, "plaintext")
        self.w.editor.add_tab("Line chart", self.line_data, "json")
        self.w.editor.add_tab("Bar chart", self.bar_data, "json")
        self.w.editor.add_tab("Data grid", self.grid_data, "json")
