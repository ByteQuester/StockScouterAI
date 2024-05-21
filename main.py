# File: general_main.py
import streamlit as st
from app.gallery.components.elements.dashboard.setup import FinancialChart
from app.gallery.ui import (DynamicInsights, KeyInsights, UIHelpers, update_sidebar)
from app.gallery.utils.data_loader import DataLoader

# Initialization
data_loader = DataLoader()
ui_helpers = UIHelpers()


def general_main():

    # ========================= Load Content =========================

    available_entities = data_loader.get_available_entities()  # Fetch entity names and CIKs
    selected_entities = st.multiselect("Select Companies", available_entities, format_func=lambda x: x[0])
    selected_ciks = [entity[1] for entity in selected_entities]
    start_date, end_date = st.sidebar.date_input("Select Date Range", [])

    if selected_ciks and start_date and end_date:
        # Load data using DataLoader
        df_assets_liabilities = data_loader.load_data_for_ciks(selected_ciks, query_type='Assets_Liabilities')
        df_cash_flow = data_loader.load_data_for_ciks(selected_ciks, query_type='Cash_Flow')
        df_profitability = data_loader.load_data_for_ciks(selected_ciks, query_type='Profitability')
        df_liquidity = data_loader.load_data_for_ciks(selected_ciks, query_type='Liquidity')

        # ========================= Main Content =========================

        # ============================  Plots  ============================
        st.subheader("Financial Charts Overview")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Assets & Liabilities", "Debt & Equity", "Cash Flow", "Profitability", "Liquidity"
        ])
        with tab1:
            with st.expander("Understanding Assets & Liabilities"):
                st.write(
                    "Assets and Liabilities are fundamental indicators of a company's financial health. This bar chart compares the current assets against current liabilities, providing insights into the company's ability to cover short-term obligations with its short-term assets.")
            FinancialChart(chart_type="bar", data=df_assets_liabilities, title="Assets vs. Liabilities", x_axis="DATE",
                           y_axis=["ASSETS_CURRENT", "LIABILITIES_CURRENT"], color='ENTITY').render(
                use_container_width=True)

        with tab2:
            with st.expander("Exploring Debt to Equity Ratio"):
                st.write(
                    "The Debt to Equity Ratio is a measure of a company's financial leverage. This line chart tracks the ratio over time, indicating how much debt a company is using to finance its assets relative to the value of shareholders' equity.")
            FinancialChart("line", df_assets_liabilities, "Debt to Equity Ratio", "DATE", "DEBT_TO_EQUITY_RATIO",
                           color='ENTITY').render()

        with tab3:
            with st.expander("Cash Flow Summary Insights"):
                st.write(
                    "Cash flow is the net amount of cash being transferred into and out of a business. This bar chart breaks down the company's cash flow into operating, investing, and financing activities, highlighting the operational efficiency and financial health.")
            FinancialChart("bar", df_cash_flow, "Cash Flow Summary", "DATE",
                           ["CASH_FLOW_OPERATING", "CASH_FLOW_INVESTING", "CASH_FLOW_FINANCING"],
                           color='ENTITY').render(use_container_width=True)

        with tab4:
            with st.expander("Profit Margin Trend Analysis"):
                st.write(
                    "Profit margin is a key indicator of a company's profitability. This line chart shows the trend of profit margin over time, offering insights into how effectively a company converts sales into net income.")
            FinancialChart(chart_type="line", data=df_profitability, title="Profit Margin Trend", x_axis="DATE",
                           y_axis="PROFIT_MARGIN", color='ENTITY').render(use_container_width=True)

        with tab5:
            with st.expander("Liquidity - Current Ratio Trend"):
                st.write(
                    "The Current Ratio is an indicator of a company's ability to pay short-term obligations. This line chart visualizes the current ratio trend, providing a snapshot of the company's short-term liquidity.")
            FinancialChart("line", df_liquidity, "Liquidity - Current Ratio Trend", "DATE", "CURRENT_RATIO",
                           color='ENTITY').render(use_container_width=True)

        st.divider()

        # ============================  Insights  ============================


if __name__ == "__main__":
    general_main()

#TODO: date and other cik att neesd to be fix
# NOTE: Proft margin trend can be used