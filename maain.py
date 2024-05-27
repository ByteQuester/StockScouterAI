import json
import streamlit as st
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
import os

from app.services.queries.query_managers.data_loader import DataLoader
from app.services.queries.query_managers.query_manager import QueryManager
from app.services.functions.transformers import TransformerManager
from app.gallery.components.elements.charts import Dashboard, Editor, Card, DataGrid, Line, Bar
from app.gallery.components.elements.dashboard.dev.widget_manager import WidgetManager
from app.services.types import (ASSETS_LIABILITIES_LINE_METRICS,
                                CASH_FLOW_CHARTS_METRICS,
                                LIQUIDITY_LINE_METRICS,
                                PROFITABILITY_LINE_METRICS)
from app.services.functions.data.post_processing.custom_transfomer import CustomTransformer  # Import the new transformer
import pandas as pd  # Ensure pandas is imported

def load_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def initialize_dashboard(config, board, editor, view_manager, cik, query_type, start_date, end_date):
    widget_manager = WidgetManager(board, editor)
    transformer_manager = TransformerManager()

    for widget_config in config:
        widget_type = widget_config["type"]
        position = widget_config["position"]
        min_size = widget_config["minSize"]
        content_key = widget_config["contentKey"]

        query_file = f'app/services/queries/sql_views/{query_type.lower()}_views.sql'
        params = (cik, start_date, end_date)
        print(f"Executing query from file: {query_file} with params: {params}")
        df = view_manager.execute_query(query_file, params)
        print("Query result dataframe:\n", df)

        if df.empty:
            print(f"No data returned for widget {content_key} of type {widget_type}")
            continue

        transformed_data = transformer_manager.transform_data(df, query_type, widget_type.lower() + "_chart")
        print(f"Transformed data for widget {content_key}:\n", transformed_data)

        if widget_type == "Line":
            widget_manager.add_widget(Line, position, min_size, content_key, transformed_data)
        elif widget_type == "Bar":
            keys = widget_config.get("keys", [])
            widget_manager.add_widget(Bar, position, min_size, content_key, transformed_data, keys=keys)
        elif widget_type == "DataGrid":
            columns = widget_config.get("columns", [])
            widget_manager.add_widget(DataGrid, position, min_size, content_key, transformed_data, columns=columns)
        elif widget_type == "Card":
            widget_manager.add_widget(Card, position, min_size, content_key, transformed_data)

    return widget_manager

def setup_sidebar():
    st.sidebar.header("Select Widgets to Display")
    show_line = st.sidebar.checkbox("Line Chart", value=True)
    show_bar = st.sidebar.checkbox("Bar Chart", value=True)
    show_data_grid = st.sidebar.checkbox("Data Grid", value=True)
    show_card = st.sidebar.checkbox("Card", value=True)
    return [key for key, value in {
        "Line chart": show_line,
        "Bar chart": show_bar,
        "Data grid": show_data_grid,
        "Card content": show_card
    }.items() if value]

def main():
    config = load_config("app/gallery/components/elements/dashboard/dev/config.json")
    dashboard_config = config.get("Profitability", [])

    data_loader = DataLoader()
    query_manager = QueryManager()
    data_loader.load_data_to_db()

    if "w" not in state:
        board = Dashboard()
        editor = Editor(board, 0, 0, 6, 11, minW=3, minH=3)
        w = SimpleNamespace(dashboard=board, editor=editor)
        state.w = w
        widget_manager = initialize_dashboard(dashboard_config, board, editor, query_manager, "0000816761",
                                              "Profitability", "2020-01-01", "2023-01-01")
        state.widget_manager = widget_manager
    else:
        w = state.w
        widget_manager = state.widget_manager

    visible_widgets = setup_sidebar()

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
        with w.dashboard(rowHeight=57):
            w.editor()
            widget_manager.render_widgets(visible_widgets)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()


