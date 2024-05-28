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
    st.sidebar.header("Resources ✨")
    st.sidebar.info(
        """The raw data is taken from [SEC](https://www.sec.gov/)""")

    # Dynamic CIK input
    available_cik = data_loader.get_available_cik_numbers()
    cik = st.sidebar.selectbox("Enter CIK Number", available_cik)
    entity_name = data_loader.get_entity_name(cik)

    # Fetch and display available query types for the given CIK
    if cik:
        available_queries = data_loader.get_available_query_types(cik)
        if available_queries:
            query_type = st.sidebar.selectbox("Select Query Type",
                                              available_queries)

            # Initialize the appropriate dashboard based on the selected query type
            if query_type:
                # Add checkboxes for widget selection
                show_card = st.sidebar.checkbox('Show Card', value=True)
                show_line = st.sidebar.checkbox('Show Line Chart')
                show_divergence_line = st.sidebar.checkbox(
                    'Show Divergence Line Chart')
                show_bar = st.sidebar.checkbox('Show Bar Chart')
                show_grid = st.sidebar.checkbox('Show Data Grid')

                selected_widgets = {
                    "card": show_card,
                    "line": show_line,
                    "divergence_line": show_divergence_line,
                    "bar": show_bar,
                    "grid": show_grid
                }

                dashboard_map = {
                    "Profitability": ProfitabilityDashboard,
                    "Assets Liabilities": AssetsLiabilitiesDashboard,
                    "Cash Flow": CashFlowDashboard,
                    "Liquidity": LiquidityDashboard
                }

                dashboard_class = dashboard_map.get(query_type)
                if dashboard_class:
                    # Initialize and render the selected dashboard with selected widgets
                    dashboard = dashboard_class(
                        cik=cik, selected_widgets=selected_widgets)
                    dashboard.render_dashboard()
                else:
                    st.error(
                        "Dashboard not found for the selected query type.")
        else:
            st.error("No available queries for this CIK.")
    else:
        st.sidebar.warning("Please select a CIK Number.")

    st.sidebar.header("About the Dashboard")
    st.sidebar.markdown("""
        Explore financial data of publicly traded companies in the US. 
        Analyze assets, liabilities, cash flow, and more through interactive visualizations.
    """)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    third_tier_main()
