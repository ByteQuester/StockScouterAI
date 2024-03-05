from abc import ABC, abstractmethod
from types import SimpleNamespace

from app.gallery.components.elements.charts import (Dashboard, DataGrid, Editor)
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
        )

    @abstractmethod
    def setup_content(self):
        pass


class LiquidityDashboardSetup(DashboardSetup):

    def __init__(self, grid_data):
        self.grid_data = grid_data
        super().__init__()
        self.initialize()

    def setup_widgets(self):
        super().setup_widgets()
        self.w.grid_chart = DataGrid(self.board,
                                     0,
                                     10,
                                     12,
                                     4,
                                     minH=4,
                                     columns=LIQUIDITY_DEFAULT_COLUMNS)

    def setup_content(self):
        self.w.editor.add_tab("Data grid", self.grid_data, "json")
