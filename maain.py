import json
from types import SimpleNamespace

import pandas as pd
import streamlit as st
from streamlit import session_state as state
from streamlit_elements import elements, event, sync

from app.gallery.components.elements.charts import (Bar, Card, Dashboard,
                                                    DataGrid, Editor, Line)
from app.gallery.components.elements.dashboard.dev.widget_manager import \
    WidgetManager
from app.services.functions.data.post_processing.custom_transfomer import \
    CustomTransformer
from app.services.queries.query_managers.data_loader import DataLoader
from app.services.queries.query_managers.sql_executor_dev import SQLExecutor
from app.services.queries.sql_views import SQL_QUERY_FILES
from app.services.types import (ASSETS_LIABILITIES_BAR_METRICS,
                                ASSETS_LIABILITIES_LINE_METRICS,
                                CASH_FLOW_CHARTS_METRICS,
                                LIQUIDITY_BAR_METRICS, LIQUIDITY_LINE_METRICS,
                                PROFITABILITY_LINE_METRICS,
                                PROFITABILITY_MARGIN_LINE_METRIC)


def load_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def get_metrics(query_type):
    metrics_map = {
        "Profitability": PROFITABILITY_LINE_METRICS.value,
        "Liquidity": LIQUIDITY_LINE_METRICS.value,
        "Assets Liabilities": ASSETS_LIABILITIES_LINE_METRICS.value,
        "Cash Flow": CASH_FLOW_CHARTS_METRICS.value
    }
    return metrics_map.get(query_type, [])


def setup_sidebar():
    st.sidebar.header("Select Widgets to Display")
    show_line = st.sidebar.checkbox("Line Chart", value=True)
    show_bar = st.sidebar.checkbox("Bar Chart", value=True)
    show_data_grid = st.sidebar.checkbox("Data Grid", value=True)
    show_card = st.sidebar.checkbox("Card", value=True)

    st.sidebar.header("Filter by CIK")
    ciks = st.sidebar.text_input("Enter CIKs separated by commas", "0000816761,0001640147")
    cik_list = [cik.strip() for cik in ciks.split(",") if cik.strip()]

    return {
        "widgets": [key for key, value in {
            "Line chart": show_line,
            "Bar chart": show_bar,
            "Data grid": show_data_grid,
            "Card content": show_card
        }.items() if value],
        "ciks": cik_list
    }

def initialize_dashboard(config, board, editor, sql_executor, query_type, ciks, start_date, end_date):
    widget_manager = WidgetManager(board, editor)

    for widget_config in config:
        widget_type = widget_config["type"]
        position = widget_config["position"]
        min_size = widget_config["minSize"]
        content_key = widget_config["contentKey"]

        query_files = SQL_QUERY_FILES.get(query_type, {})
        for query_name, query_file in query_files.items():
            sql_executor.execute_sql_file(query_file)

        placeholders = ', '.join(['?'] * len(ciks))
        query_sql = f"SELECT * FROM profitability_analysis WHERE CIK IN ({placeholders}) AND DATE BETWEEN ? AND ?"
        params = (*ciks, start_date, end_date)
        query_result = sql_executor.query_sql(query_sql, params)
        print("Query result list of dicts:\n", query_result)

        if not query_result:
            print(f"No data returned for widget {content_key} of type {widget_type}")
            continue

        df = pd.DataFrame(query_result)
        print("Converted DataFrame:\n", df)

        if df.empty:
            print(f"No data returned for widget {content_key} of type {widget_type}")
            continue

        metrics = get_metrics(query_type)
        custom_transformer = CustomTransformer(df, metrics)
        transformed_data = custom_transformer.transform_all()
        print(f"Transformed data for widget {content_key}:\n", transformed_data)

        if widget_type == "Line":
            widget_manager.add_widget(Line, position, min_size, content_key, transformed_data["line_chart"])
        elif widget_type == "Bar":
            keys = widget_config.get("keys", [])
            widget_manager.add_widget(Bar, position, min_size, content_key, transformed_data["bar_chart"], keys=keys)
        elif widget_type == "DataGrid":
            columns = widget_config.get("columns", [])
            widget_manager.add_widget(DataGrid, position, min_size, content_key, transformed_data["data_grid"], columns=columns)
        elif widget_type == "Card":
            widget_manager.add_widget(Card, position, min_size, content_key, transformed_data["line_chart"])

    return widget_manager

def main():
    config = load_config("app/gallery/components/elements/dashboard/dev/config.json")
    dashboard_config = config.get("Profitability", [])

    data_loader = DataLoader()
    data_loader.load_data_to_db()

    if "w" not in state:
        board = Dashboard()
        editor = Editor(board, 0, 0, 6, 11, minW=3, minH=3)
        w = SimpleNamespace(dashboard=board, editor=editor)
        state.w = w
        sql_executor = SQLExecutor('data.db')
        sidebar_config = setup_sidebar()
        ciks = sidebar_config["ciks"]
        visible_widgets = sidebar_config["widgets"]
        widget_manager = initialize_dashboard(dashboard_config, board, editor, sql_executor, "Profitability", ciks, "2020-01-01", "2023-01-01")
        state.widget_manager = widget_manager
    else:
        w = state.w
        widget_manager = state.widget_manager
        visible_widgets = setup_sidebar()["widgets"]

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
        with w.dashboard(rowHeight=57):
            w.editor()
            widget_manager.render_widgets(visible_widgets)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
