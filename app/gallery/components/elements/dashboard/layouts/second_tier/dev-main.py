# File: main.py
import streamlit as st
from app.gallery.components.elements.dashboard.layouts.second_tier import (
    AssetsLiabilitiesDashboardDev, CashFlowDashboardDev, LiquidityDashboardDev, ProfitabilityDashboardDev)
from app.gallery.utils import DataLoader


def second_tier_main():
    data_loader = DataLoader()

    st.sidebar.header("About the Dashboard")
    st.sidebar.markdown("""
        Detailed financial analysis across various metrics. 
        Explore in-depth insights into profitability, cash flow, assets & liabilities, and liquidity.
    """)
    st.sidebar.header("Resources ✨")
    st.sidebar.info("The raw data is taken from [SEC](https://www.sec.gov/)")

    with st.expander("Quick Info"):
        st.write("""
            1. **Select Companies**: Use the multi-select to choose companies by their CIK numbers.
            2. **Explore Tabs**: Navigate through different financial aspects in the tabs.
            3. **Dynamic Insights**: Uncover tailored insights and observations about financial trends.
        """)

    available_entities = data_loader.get_available_entities()  # Assuming this method returns a list of (entity_name, cik) tuples
    selected_entities = st.multiselect("Select Companies", available_entities, format_func=lambda x: x[0])
    selected_ciks = [entity[1] for entity in selected_entities]
    start_date, end_date = st.sidebar.date_input("Select Date Range", [])

    if selected_ciks and start_date and end_date:
        available_queries = ["Profitability", "Cash Flow", "Assets & Liabilities", "Liquidity"]
        query_type = st.selectbox("Select Query Type", available_queries)
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
            st.error("Selected query type is not supported or not implemented yet.")


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
