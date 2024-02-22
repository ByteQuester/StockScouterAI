import streamlit as st

from app.gallery.components.elements.dashboard.layouts.third_tier import (
    AssetsLiabilitiesDashboard, CashFlowDashboard, LiquidityDashboard,
    ProfitabilityDashboard)
from app.gallery.ui import UIHelpers
from app.gallery.utils import DataLoader

data_loader = DataLoader()
ui_helpers = UIHelpers()


def third_tier_main():
    # ========================= Sidebar =========================
    st.sidebar.header("About the Dashboard")
    st.sidebar.markdown("""
        Explore financial data of publicly traded companies in the US. 
        Analyze assets, liabilities, cash flow, and more through interactive visualizations.
    """)

    st.sidebar.header("Resources ✨")
    st.sidebar.info(
        """The raw data is taken from [SEC](https://www.sec.gov/)""")

    # ========================= Main Content =========================
    # Quick guide
    with st.expander("Quick Info"):
        st.write(
            "1. **Select a Company**: Use the drop-down to choose a company by its CIK number.\n"
            "2. **Explore Tabs**: Navigate through different financial aspects in the tabs.\n"
            "3. **Dynamic Insights**: Uncover tailored insights and observations about financial trends."
        )

    # Dynamic CIK input
    available_cik = data_loader.get_available_cik_numbers()
    cik = st.selectbox("Enter CIK Number", available_cik)
    entity_name = data_loader.get_entity_name(cik)

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
        # Fetch and display available query types for the given CIK
        available_queries = data_loader.get_available_query_types(cik)
        if available_queries:
            query_type = st.selectbox("Select Query Type", available_queries)

            # Initialize the appropriate dashboard based on the selected query type
            if query_type:
                dashboard_map = {
                    "Profitability": ProfitabilityDashboard,
                    "Assets Liabilities": AssetsLiabilitiesDashboard,
                    "Cash Flow": CashFlowDashboard,
                    "Liquidity": LiquidityDashboard
                }

                dashboard_class = dashboard_map.get(query_type)
                if dashboard_class:
                    # Initialize and render the selected dashboard
                    dashboard = dashboard_class(cik=cik)
                    dashboard.render_dashboard()
                else:
                    st.error(
                        "Dashboard not found for the selected query type.")
        else:
            st.error("No available queries for this CIK.")


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    third_tier_main()
