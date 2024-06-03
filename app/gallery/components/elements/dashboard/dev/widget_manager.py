import json
from typing import List, Tuple, Type


class WidgetManager:
    """
    Manages the widgets on the dashboard, allowing the addition and rendering of widgets.

    Attributes:
        board: The dashboard board object where widgets will be placed.
        editor: The editor object for managing widget content.
        widgets: A list of tuples containing widget instances and their corresponding content keys.
    """

    def __init__(self, board, editor) -> None:
        """
        Initializes the WidgetManager with the specified board and editor.

        Args:
            board: The dashboard board object.
            editor: The editor object.
        """
        self.board = board
        self.editor = editor
        self.widgets: List[Tuple] = []

    def add_widget(self, widget_cls: Type, position: Tuple[int, int], min_size: Tuple[int, int], content_key: str, data: str,
                   content_type : str = "json",
                   **kwargs) -> None:
        """
        Adds a widget to the dashboard.

        Args:
            widget_cls: The widget class to instantiate.
            position: The (x, y) position of the widget on the dashboard.
            min_size: The (min_width, min_height) of the widget.
            content_key: The key for the content to be displayed in the widget.
            data: The data to be displayed in the widget.
            content_type: The type of content, either "json" or "plain text".
            **kwargs: Additional keyword arguments to be passed to the widget.
        """
        widget = widget_cls(self.board,
                            *position,
                            minW=min_size[0],
                            minH=min_size[1],
                            **kwargs)
        formatted_data = json.dumps(data, indent=2) if content_type == "json" else data
        self.editor.add_tab(content_key, formatted_data, content_type)
        self.widgets.append((widget, content_key))

    def render_widgets(self, visible_widgets: List[str]) -> None:
        """
        Renders the widgets on the dashboard.

        Args:
            visible_widgets: A list of content keys for widgets that should be visible.
        """
        for widget, content_key in self.widgets:
            if content_key in visible_widgets:
                widget(self.editor.get_content(content_key))
