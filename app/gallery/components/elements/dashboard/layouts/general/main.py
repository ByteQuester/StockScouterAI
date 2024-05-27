# general_main.py

import streamlit as st

from app.gallery.components.elements.dashboard.layouts.general.general_dashboard import \
    GeneralDashboardBase
from app.gallery.ui import UIHelpers, update_sidebar
from app.gallery.utils.data_loader import DataLoader


def general_main():
    st.sidebar.header("Resources ✨")
    st.sidebar.info("The raw data is taken from [SEC](https://sec.gov)")
    update_sidebar()
    data_loader = DataLoader()
    available_entities = data_loader.get_available_entities()
    selected_entities = st.sidebar.multiselect("Select Companies",
                                               available_entities,
                                               format_func=lambda x: x[0])
    selected_ciks = [entity[1] for entity in selected_entities]

    view_type = st.sidebar.selectbox("Select View Type",
                                     ["Grouped", "Stacked", "Subplots"])

    if selected_ciks:
        dashboard = GeneralDashboardBase(selected_ciks, 'general')
        dashboard.initialize_analysis()
        chart_selection = dashboard.render_sidebar()
        dashboard.render_tabs(chart_selection, view_type)

    st.sidebar.header("About the Dashboard")
    st.sidebar.markdown("""
        Explore financial data of publicly traded companies in the US. 
        Analyze assets, liabilities, cash flow, and more through interactive visualizations.
    """)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    general_main()
