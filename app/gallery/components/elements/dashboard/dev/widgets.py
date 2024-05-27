from streamlit_elements import mui

# Assuming these are imported
from app.gallery.components.elements.charts import Line, Bar, DataGrid, Editor


def create_widget(board, config):
    widget_type = config["type"]
    position = config["position"]
    min_size = config["minSize"]
    content_key = config["contentKey"]

    if widget_type == "Line":
        widget = Line(board, *position, minW=min_size[0], minH=min_size[1])
    elif widget_type == "Bar":
        widget = Bar(board, *position, minW=min_size[0], minH=min_size[1])
    elif widget_type == "DataGrid":
        widget = DataGrid(board, *position, minW=min_size[0], minH=min_size[1])
    else:
        raise ValueError(f"Unsupported widget type: {widget_type}")

    # Assuming widgets can fetch and update their content from an Editor instance
    widget.content = editor.get_content(content_key)  # Editor instance to be passed or globally accessible
    return widget

def initialize_dashboard(board, config):
    widgets = []
    for widget_config in config["Profitability"]:
        widget = create_widget(board, widget_config)
        widgets.append(widget)
    return widgets
