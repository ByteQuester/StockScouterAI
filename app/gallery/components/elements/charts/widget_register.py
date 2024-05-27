# widget_registry.py

from .bar import Bar
from .card import Card
from .datagrid import DataGrid
from .editor import Editor
from .line import Line
from .pie import Pie
from .player import Player

WIDGET_REGISTRY = {
    'Bar Chart': Bar,
    'Card': Card,
    'Data Grid': DataGrid,
    'Editor': Editor,
    'Line Chart': Line,
    'Pie Chart': Pie,
    'Media Player': Player,
}

def create_widget(widget_name, *args, **kwargs):
    widget_class = WIDGET_REGISTRY.get(widget_name)
    if widget_class:
        return widget_class(*args, **kwargs)
    else:
        raise ValueError(f"Unknown widget: {widget_name}")
