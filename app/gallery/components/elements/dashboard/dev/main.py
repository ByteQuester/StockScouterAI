import json
import streamlit as st
from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace

from app.gallery.components.elements.charts import Dashboard, Editor, Card, DataGrid, Line, Bar

def load_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def main():

    config = load_config("app/gallery/components/elements/dashboard/dev/config.json")
    dashboard_config = config.get("Profitability", [])

    if "w" not in state:
        board = Dashboard()
        w = SimpleNamespace(dashboard=board)
        state.w = w

        for widget_config in dashboard_config:
            widget_type = widget_config["type"]
            position = widget_config["position"]
            min_size = widget_config["minSize"]
            content_key = widget_config["contentKey"]

            if widget_type == "Line":
                w.line = Line(board, *position, minW=min_size[0], minH=min_size[1])
                w.editor.add_tab(content_key, json.dumps(Line.DEFAULT_DATA, indent=2), "json")
            elif widget_type == "Bar":
                w.bar = Bar(board, *position, minW=min_size[0], minH=min_size[1])
                w.editor.add_tab(content_key, json.dumps(Bar.DEFAULT_DATA, indent=2), "json")
            elif widget_type == "DataGrid":
                w.data_grid = DataGrid(board, *position, minW=min_size[0], minH=min_size[1])
                w.editor.add_tab(content_key, json.dumps(DataGrid.DEFAULT_ROWS, indent=2), "json")
            elif widget_type == "Card":
                w.card = Card(board, *position, minW=min_size[0], minH=min_size[1])
                w.editor.add_tab(content_key, Card.DEFAULT_CONTENT, "plaintext")

    else:
        w = state.w

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            w.editor()
            if hasattr(w, "line"):
                w.line(w.editor.get_content("Line chart"))
            if hasattr(w, "bar"):
                w.bar(w.editor.get_content("Bar chart"))
            if hasattr(w, "data_grid"):
                w.data_grid(w.editor.get_content("Data grid"))
            if hasattr(w, "card"):
                w.card(w.editor.get_content("Card content"))

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
