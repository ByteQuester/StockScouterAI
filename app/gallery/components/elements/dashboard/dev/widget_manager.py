import json


class WidgetManager:

    def __init__(self, board, editor):
        self.board = board
        self.editor = editor
        self.widgets = []

    def add_widget(self, widget_cls, position, min_size, content_key, data,
                   **kwargs):
        widget = widget_cls(self.board,
                            *position,
                            minW=min_size[0],
                            minH=min_size[1],
                            **kwargs)
        self.editor.add_tab(content_key, json.dumps(data, indent=2), "json")
        self.widgets.append((widget, content_key))

    def render_widgets(self, visible_widgets):
        for widget, content_key in self.widgets:
            if content_key in visible_widgets:
                widget(self.editor.get_content(content_key))
