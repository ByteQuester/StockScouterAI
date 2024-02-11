import streamlit as st

from app.gallery.components.elements.dashboard.layouts import (
    AssetsLiabilitiesDashboard, CashFlowDashboard, LiquidityDashboard,
    ProfitabilityDashboard)
from app.gallery.ui import UIHelpers
from app.gallery.utils import DataLoader

data_loader = DataLoader()
ui_helpers = UIHelpers()


def main():
    # Dynamic CIK input
    available_cik = data_loader.get_available_cik_numbers()
    cik = st.selectbox("Enter CIK Number", available_cik)

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
    main()
