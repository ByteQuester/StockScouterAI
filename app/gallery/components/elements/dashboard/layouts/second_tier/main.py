import streamlit as st

from app.gallery.components.elements.dashboard.layouts.second_tier import (
    AssetsLiabilitiesDashboardDev, CashFlowDashboardDev, LiquidityDashboardDev,
    ProfitabilityDashboardDev)
from app.gallery.utils import DataLoader


def second_tier_main():
    # Set page configuration and style

    # ========================= Initialization =========================
    # Initialize utilities
    data_loader = DataLoader()

    # ========================= Sidebar =========================
    # Sidebar - Additional Information
    st.sidebar.header("About the Dashboard")
    st.sidebar.markdown("""
        Detailed financial analysis across various metrics. 
        Explore in-depth insights into profitability, cash flow, assets & liabilities, and liquidity.
    """)

    # ========================= Main Content =========================
    # Quick guide
    with st.expander("Quick Info"):
        st.write(
            "1. **Select a Company**: Use the drop-down to choose a company by its CIK number.\n"
            "2. **Explore Tabs**: Navigate through different financial aspects in the tabs.\n"
            "3. **Dynamic Insights**: Uncover tailored insights and observations about financial trends."
        )
    # Dynamic CIK Selection from Sidebar
    available_cik = data_loader.get_available_cik_numbers()
    cik = st.selectbox("Select CIK", available_cik)
    entity_name = data_loader.get_entity_name(cik)
    # Display Dashboard Title and Header
    # Display title and header
    c1, c2 = st.columns([0.2, 3.5], gap="large")
    with c1:
        st.image(
            'icon.png',
            width=80,
        )

    with c2:
        st.title(f'{entity_name} Overview Dashboard')
        st.markdown("*Visualizing General Levels*")
    st.divider()

    if cik:
        # Dynamic Query Type Selection
        available_queries = [
            "Profitability", "Cash Flow", "Assets & Liabilities", "Liquidity"
        ]
        query_type = st.selectbox("Select Query Type", available_queries)
        # Map query types to corresponding analysis classes
        query_to_class_mapping = {
            "Profitability": ProfitabilityDashboardDev,
            "Cash Flow": CashFlowDashboardDev,
            "Assets & Liabilities": AssetsLiabilitiesDashboardDev,
            "Liquidity": LiquidityDashboardDev
        }
        # Initialize and run the selected analysis
        analysis_class = query_to_class_mapping.get(query_type)
        if analysis_class:
            analysis = analysis_class(cik)
            run_selected_analysis(analysis)
        else:
            st.error(
                "Selected query type is not supported or not implemented yet.")


def run_selected_analysis(analysis):
    # ========================= Data Loading and Filtering =========================
    analysis.load_data()

    # Defining and selecting the date range
    start_date, end_date = analysis.select_date_range()
    if start_date and end_date:
        analysis.filter_data_by_date(start_date, end_date)

        # ========================= Analysis Initialization and Rendering =========================
        try:
            analysis.initialize_analysis()
            analysis.render_charts()
        except ValueError as e:
            st.error(f"Error in analysis initialization: {e}")
    else:
        st.error("Please select a valid date range.")


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    second_tier_main()
