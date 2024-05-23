# File: main.py
import streamlit as st

from app.gallery.components.elements.dashboard.layouts.second_tier import (
    AssetsLiabilitiesDashboardDev, CashFlowDashboardDev, LiquidityDashboardDev,
    ProfitabilityDashboardDev)
from app.gallery.ui import UIHelpers
from app.gallery.utils import DataLoader


def second_tier_main():
    st.sidebar.header("Resources ✨")
    st.sidebar.info("The raw data is taken from [SEC](https://www.sec.gov/)")

    data_loader = DataLoader()
    available_entities = data_loader.get_available_entities()
    selected_entities = st.sidebar.multiselect("Select Companies",
                                               available_entities,
                                               format_func=lambda x: x[0])
    selected_ciks = [entity[1] for entity in selected_entities]

    date_on_sidebar = UIHelpers.switch("Show Date Range Selector on Sidebar",
                                       default_value=True,
                                       in_sidebar=True)
    if date_on_sidebar:
        start_date, end_date = UIHelpers.select_date_range(in_sidebar=True)
    else:
        start_date, end_date = UIHelpers.select_date_range(in_sidebar=False)

    if selected_ciks and start_date and end_date:
        available_queries = [
            "Profitability", "Cash Flow", "Assets & Liabilities", "Liquidity"
        ]
        query_type = st.sidebar.selectbox("Select Query Type",
                                          available_queries)
        query_to_class_mapping = {
            "Profitability": ProfitabilityDashboardDev,
            "Cash Flow": CashFlowDashboardDev,
            "Assets & Liabilities": AssetsLiabilitiesDashboardDev,
            "Liquidity": LiquidityDashboardDev
        }
        analysis_class = query_to_class_mapping.get(query_type)
        if analysis_class:
            analysis = analysis_class(selected_ciks)
            run_selected_analysis(analysis, start_date, end_date)
        else:
            st.error(
                "Selected query type is not supported or not implemented yet.")

    st.sidebar.header("About")
    st.sidebar.markdown("""
        Detailed financial analysis across various metrics. 
        Explore in-depth insights into profitability, cash flow, assets & liabilities, and liquidity.
    """)


def run_selected_analysis(analysis, start_date, end_date):
    analysis.load_data()
    analysis.filter_data_by_date(start_date, end_date)
    try:
        analysis.initialize_analysis()
        analysis.render_charts()
    except ValueError as e:
        st.error(f"Error in analysis initialization: {e}")


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    second_tier_main()
