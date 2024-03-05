from abc import ABC, abstractmethod
from types import SimpleNamespace

from app.gallery.components.elements.charts import (Dashboard, Bar, Editor)


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
            bar=Bar(self.board, 0, 6, 6, 4, minW=2, minH=4),
        )

    @abstractmethod
    def setup_content(self):
        pass


class LiquidityDashboardSetup(DashboardSetup):

    def __init__(self, bar_data):
        self.bar_data = bar_data
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

    def setup_content(self):
        self.w.editor.add_tab("Bar chart", self.bar_data, "json")
