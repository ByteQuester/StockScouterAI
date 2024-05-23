import streamlit as st

from app.gallery.components.elements.dashboard.setup import FinancialChart
from app.gallery.ui import (DynamicInsights, KeyInsights, UIHelpers,
                            update_sidebar)
from app.gallery.utils.data_loader import DataLoader

# Initialization
data_loader = DataLoader()
ui_helpers = UIHelpers()


def general_main():
    # Set page configuration and style
    st.markdown("""<style>.insight-box {...}</style>""",
                unsafe_allow_html=True)

    # ========================= Sidebar =========================
    # Markdowns
    st.sidebar.header("About the Dashboard")
    st.sidebar.markdown("""
        Explore financial data of publicly traded companies in the US. 
        Analyze assets, liabilities, cash flow, and more through interactive visualizations.
    """)
    st.sidebar.header("Resources ✨")
    st.sidebar.info("""The raw data is taken from [SEC](https://sec.gov).""")
    # Initialize and update sidebar
    update_sidebar()

    # ========================= Load Content =========================
    # Quick guide
    with st.expander("Quick Info"):
        st.write(
            "1. **Select a Company**: Use the drop-down to choose a company by its CIK number.\n"
            "2. **Explore Tabs**: Navigate through different financial aspects in the tabs.\n"
            "3. **Dynamic Insights**: Uncover tailored insights and observations about financial trends."
        )

    # CIK selection
    available_cik = data_loader.get_available_cik_numbers()
    cik = st.selectbox("Select CIK", available_cik)
    entity_name = data_loader.get_entity_name(cik)
    # Load data using DataLoader
    df_assets_liabilities = data_loader.load_csv_data(
        cik, query_type='Assets_Liabilities')
    df_cash_flow = data_loader.load_csv_data(cik, query_type='Cash_Flow')
    df_profitability = data_loader.load_csv_data(cik,
                                                 query_type='Profitability')
    df_liquidity = data_loader.load_csv_data(cik, query_type='Liquidity')
    # Define the configuration for Key Insights
    insights_data = {
        'total_assets':
        f"{df_assets_liabilities['ASSETS_CURRENT'].iloc[-1]} mil $",
        'total_liabilities':
        f"{df_assets_liabilities['LIABILITIES_CURRENT'].iloc[-1]} mil $",
        'current_ratio': df_liquidity['CURRENT_RATIO'].iloc[-1],
        'profit_margin': f"{df_profitability['PROFIT_MARGIN'].iloc[-1]}%"
    }
    insights_config = [{
        'title': 'Total Assets',
        'data_key': 'total_assets'
    }, {
        'title': 'Total Liabilities',
        'data_key': 'total_liabilities'
    }, {
        'title': 'Current Ratio',
        'data_key': 'current_ratio',
        'format': '{value:.2f}'
    }, {
        'title': 'Profit Margin',
        'data_key': 'profit_margin'
    }]
    # Define the configuration for dynamic insights
    data_insights = [
        {
            'label':
            'Profit Margin Trend',
            'calculation':
            lambda: "increasing" if df_profitability['PROFIT_MARGIN'].iloc[-1]
            > df_profitability['PROFIT_MARGIN'].iloc[0] else "decreasing",
            'positive_outcomes': ['increasing'],
            'explanation':
            'An increasing trend suggests that the company is becoming more efficient in converting sales into actual profit, indicating financial health.'
        },
        {
            'label':
            'Cash Flow Health',
            'calculation':
            lambda: "healthy" if df_cash_flow['CASH_FLOW_OPERATING'].iloc[-1] >
            0 else "concerning",
            'positive_outcomes': ['healthy'],
            'explanation':
            ' Positive cash flow from operations signifies a company solid financial position, ensuring it can meet its obligations and invest in growth.'
        },
        {
            'label':
            'Liquidity Position',
            'calculation':
            lambda: "good"
            if df_liquidity['CURRENT_RATIO'].iloc[-1] > 1 else "poor",
            'positive_outcomes': ['good'],
            'explanation':
            'A current ratio above 1 indicates that the company has more current assets than current liabilities, suggesting good short-term financial stability.'
        },
        {
            'label':
            'Leverage Situation',
            'calculation':
            lambda: "increasing risk" if df_assets_liabilities[
                'DEBT_TO_EQUITY_RATIO'].iloc[-1] > df_assets_liabilities[
                    'DEBT_TO_EQUITY_RATIO'].iloc[0] else "stable",
            'positive_outcomes': ['stable'],
            'explanation':
            'A stable or low debt-to-equity ratio indicates that the company is not overly reliant on debt financing, reducing financial risk.'
        },
    ]
    # ========================= Main Content =========================
    # Display Dashboard Title
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
    st.header('Key Financial Insights')
    st.divider()
    # Render key insights
    key_insights = KeyInsights(insights_data, insights_config)
    key_insights.render()
    st.divider()

    # ============================  Plots  ============================
    st.subheader("Financial Charts Overview")
    st.info(
        """Explore comprehensive financial insights through interactive charts. Each chart below represents a key aspect of the company's financial health, enabling a deeper understanding of its financial stability, efficiency, and growth prospects"""
    )
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Assets & Liabilities", "Debt & Equity", "Cash Flow", "Profitability",
        "Liquidity"
    ])
    with tab1:
        with st.expander("Understanding Assets & Liabilities"):
            st.write(
                "Assets and Liabilities are fundamental indicators of a company's financial health. This bar chart compares the current assets against current liabilities, providing insights into the company's ability to cover short-term obligations with its short-term assets."
            )

        FinancialChart(chart_type="bar",
                       data=df_assets_liabilities,
                       title="Assets vs. Liabilities",
                       x_axis="DATE",
                       y_axis=["ASSETS_CURRENT", "LIABILITIES_CURRENT"
                               ]).render(use_container_width=True)
    with tab2:
        with st.expander("Exploring Debt to Equity Ratio"):
            st.write(
                "The Debt to Equity Ratio is a measure of a company's financial leverage. This line chart tracks the ratio over time, indicating how much debt a company is using to finance its assets relative to the value of shareholders' equity."
            )
        FinancialChart("line", df_assets_liabilities, "Debt to Equity Ratio",
                       "DATE", "DEBT_TO_EQUITY_RATIO").render()

    with tab3:
        with st.expander("Cash Flow Summary Insights"):
            st.write(
                " Cash flow is the net amount of cash being transferred into and out of a business. This bar chart breaks down the company's cash flow into operating, investing, and financing activities, highlighting the operational efficiency and financial health."
            )
        x = FinancialChart("bar", df_cash_flow, "Cash Flow Summary", "DATE", [
            "CASH_FLOW_OPERATING", "CASH_FLOW_INVESTING", "CASH_FLOW_FINANCING"
        ]).render(use_container_width=True)
    with tab4:
        with st.expander("Profit Margin Trend Analysis"):
            st.write(
                "Profit margin is a key indicator of a company's profitability. This line chart shows the trend of profit margin over time, offering insights into how effectively a company converts sales into net income."
            )
        FinancialChart(chart_type="line",
                       data=df_profitability,
                       title="Profit Margin Trend",
                       x_axis="DATE",
                       y_axis="PROFIT_MARGIN").render(use_container_width=True)

    with tab5:
        with st.expander("Liquidity - Current Ratio Trend"):
            st.write(
                "The Current Ratio is an indicator of a company's ability to pay short-term obligations. This line chart visualizes the current ratio trend, providing a snapshot of the company's short-term liquidity."
            )
        FinancialChart("line", df_liquidity, "Liquidity - Current Ratio Trend",
                       "DATE",
                       "CURRENT_RATIO").render(use_container_width=True)
    st.divider()

    # ============================  Insights  ============================
    st.subheader("Observations")
    st.success(
        "The Observations are purely educational and for academic purposes. No one is advised on taking financial decisions off these data points solely."
    )
    for insight in data_insights:
        dynamic_insights = DynamicInsights([insight])
        dynamic_insights.render()
        st.markdown("---")


if __name__ == "__main__":
    general_main()
