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
    CustomTransformer  # Import CustomTransformer
from app.services.functions.transformers import TransformerManager
from app.services.queries.query_managers.data_loader import DataLoader
from app.services.queries.query_managers.query_manager import QueryManager
from app.services.queries.query_managers.sql_executor import \
    SQLExecutor  # Import the new SQLExecutor
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


def initialize_dashboard(config, board, editor, view_manager, cik, query_type,
                         start_date, end_date):
    widget_manager = WidgetManager(board, editor)
    sql_executor = SQLExecutor(
        view_manager.db_path)  # Use the same database path

    for widget_config in config:
        widget_type = widget_config["type"]
        position = widget_config["position"]
        min_size = widget_config["minSize"]
        content_key = widget_config["contentKey"]

        query_file = f'app/services/queries/sql_views/{query_type.lower()}_views.sql'
        params = (cik, start_date, end_date)
        print(f"Executing query from file: {query_file} with params: {params}")

        # Execute each view creation separately
        qoq_growth_sql = """
        CREATE VIEW IF NOT EXISTS profitability_qoq_growth AS
        WITH preprocessed_data AS (
            SELECT *,
                   LAG(REVENUES, 1) OVER (PARTITION BY Entity ORDER BY DATE) AS Prev_Revenues,
                   LAG(OPS_INCOME_LOSS, 1) OVER (PARTITION BY Entity ORDER BY DATE) AS Prev_OperatingIncomeLoss
            FROM raw_profitability
        )
        SELECT
            Entity,
            CIK,
            DATE,
            Year,
            Quarter,
            NET_INCOME_LOSS,
            REVENUES,
            OPS_INCOME_LOSS,
            PROFIT_MARGIN,
            CASE WHEN Prev_Revenues IS NOT NULL AND Prev_Revenues != 0 THEN
                ROUND ((REVENUES - Prev_Revenues) / Prev_Revenues * 100, 2)
                ELSE NULL END AS Revenues_QoQ_Growth,
            CASE WHEN Prev_OperatingIncomeLoss IS NOT NULL AND Prev_OperatingIncomeLoss != 0 THEN
                ROUND ((OPS_INCOME_LOSS - Prev_OperatingIncomeLoss) / Prev_OperatingIncomeLoss * 100, 2)
                ELSE NULL END AS OperatingIncome_QoQ_Growth
        FROM preprocessed_data;
        """
        sql_executor.execute_sql(qoq_growth_sql)

        expense_ratio_sql = """
        CREATE VIEW IF NOT EXISTS profitability_expense_ratio AS
        SELECT *,
               ROUND ((REVENUES - OPS_INCOME_LOSS) / REVENUES * 100, 2) AS Expense_Ratio
        FROM raw_profitability;
        """
        sql_executor.execute_sql(expense_ratio_sql)

        analysis_sql = """
        CREATE VIEW IF NOT EXISTS profitability_analysis AS
        SELECT a.Entity,
               a.CIK,
               a.DATE,
               a.Year,
               a.Quarter,
               a.NET_INCOME_LOSS,
               a.REVENUES,
               a.OPS_INCOME_LOSS,
               a.PROFIT_MARGIN,
               b.Revenues_QoQ_Growth,
               b.OperatingIncome_QoQ_Growth,
               c.Expense_Ratio,
               a.REVENUES - a.OPS_INCOME_LOSS AS Operational_Expenses
        FROM raw_profitability a
        LEFT JOIN profitability_qoq_growth b ON a.CIK = b.CIK AND a.DATE = b.DATE
        LEFT JOIN profitability_expense_ratio c ON a.CIK = c.CIK AND a.DATE = c.DATE;
        """
        sql_executor.execute_sql(analysis_sql)

        query_sql = "SELECT * FROM profitability_analysis WHERE CIK = ? AND DATE BETWEEN ? AND ?"
        query_result = sql_executor.query_sql(query_sql, params)
        print("Query result list of dicts:\n", query_result)

        if not query_result:
            print(
                f"No data returned for widget {content_key} of type {widget_type}"
            )
            continue

        df = pd.DataFrame(query_result)
        print("Converted DataFrame:\n", df)

        if df.empty:
            print(
                f"No data returned for widget {content_key} of type {widget_type}"
            )
            continue

        metrics = get_metrics(query_type)
        custom_transformer = CustomTransformer(df, metrics)
        transformed_data = custom_transformer.transform_all()
        print(f"Transformed data for widget {content_key}:\n",
              transformed_data)

        if widget_type == "Line":
            widget_manager.add_widget(Line, position, min_size, content_key,
                                      transformed_data["line_chart"])
        elif widget_type == "Bar":
            keys = widget_config.get("keys", [])
            widget_manager.add_widget(Bar,
                                      position,
                                      min_size,
                                      content_key,
                                      transformed_data["bar_chart"],
                                      keys=keys)
        elif widget_type == "DataGrid":
            columns = widget_config.get("columns", [])
            widget_manager.add_widget(DataGrid,
                                      position,
                                      min_size,
                                      content_key,
                                      transformed_data["data_grid"],
                                      columns=columns)
        elif widget_type == "Card":
            widget_manager.add_widget(Card, position, min_size, content_key,
                                      transformed_data["line_chart"])

    return widget_manager


def setup_sidebar():
    st.sidebar.header("Select Widgets to Display")
    show_line = st.sidebar.checkbox("Line Chart", value=True)
    show_bar = st.sidebar.checkbox("Bar Chart", value=True)
    show_data_grid = st.sidebar.checkbox("Data Grid", value=True)
    show_card = st.sidebar.checkbox("Card", value=True)
    return [
        key for key, value in {
            "Line chart": show_line,
            "Bar chart": show_bar,
            "Data grid": show_data_grid,
            "Card content": show_card
        }.items() if value
    ]


def main():
    config = load_config(
        "app/gallery/components/elements/dashboard/dev/config.json")
    dashboard_config = config.get("Profitability", [])

    data_loader = DataLoader()
    query_manager = QueryManager()
    data_loader.load_data_to_db()

    if "w" not in state:
        board = Dashboard()
        editor = Editor(board, 0, 0, 6, 11, minW=3, minH=3)
        w = SimpleNamespace(dashboard=board, editor=editor)
        state.w = w
        widget_manager = initialize_dashboard(dashboard_config, board, editor,
                                              query_manager, "0000816761",
                                              "Profitability", "2020-01-01",
                                              "2023-01-01")
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
