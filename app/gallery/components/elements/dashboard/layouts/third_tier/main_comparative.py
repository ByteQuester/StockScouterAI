import streamlit as st

from app.gallery.components.elements.dashboard.layouts.third_tier import ProfitabilityLineDashboard
from app.gallery.ui import UIHelpers
from app.gallery.utils import DataLoader

data_loader = DataLoader()
ui_helpers = UIHelpers()


def comparative_third_tier_main():
    # ========================= Main Content =========================
    # Static CIK input
    cik = 'comparative'

    if cik:
        query_type = 'Profitability'

        if query_type:
            dashboard_map = {
                "Profitability": ProfitabilityLineDashboard
            }
            dashboard_class = dashboard_map.get(query_type)
            if dashboard_class:
                dashboard = dashboard_class(cik=cik)
                dashboard.render_dashboard()
            else:
                st.error("No available queries for this CIK.")

    else:
        st.error("No available queries for this CIK.")


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    comparative_third_tier_main()
