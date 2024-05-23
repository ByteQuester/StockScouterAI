# graph_renderers.py
from .chart_config import FinancialChart
from .chart_register import register_chart


def render_assets_vs_liabilities_chart(df_assets_vs_liabilities,
                                       view_type='Grouped'):
    bar_mode = 'group' if view_type == 'Grouped' else 'stack'
    color = 'ENTITY' if view_type != 'Subplots' else None

    FinancialChart(chart_type="bar",
                   data=df_assets_vs_liabilities,
                   title="Assets vs. Liabilities",
                   x_axis="DATE",
                   y_axis=["ASSETS_CURRENT", "LIABILITIES_CURRENT"],
                   bar_mode=bar_mode,
                   color=color,
                   bargap=0.15,
                   bargroupgap=0.1).render()

    if view_type == 'Subplots':
        # Additional logic to create subplots for different metrics
        metrics = ["ASSETS_CURRENT", "LIABILITIES_CURRENT"]
        for metric in metrics:
            FinancialChart(chart_type="bar",
                           data=df_assets_vs_liabilities,
                           title=f"{metric} over Time",
                           x_axis="DATE",
                           y_axis=metric,
                           color='ENTITY',
                           bargap=0.15,
                           bargroupgap=0.1).render()


def render_debt_to_equity_chart(df_assets_liabilities):
    FinancialChart(chart_type="line",
                   data=df_assets_liabilities,
                   title="Debt to Equity Ratio",
                   x_axis="DATE",
                   y_axis="DEBT_TO_EQUITY_RATIO").render()


def render_cash_flow_summary_chart(df_cash_flow, view_type='Grouped'):
    bar_mode = 'group' if view_type == 'Grouped' else 'stack'
    color = 'ENTITY' if view_type != 'Subplots' else None

    FinancialChart(chart_type="bar",
                   data=df_cash_flow,
                   title="Cash Flow Summary",
                   x_axis="DATE",
                   y_axis=[
                       "CASH_FLOW_OPERATING", "CASH_FLOW_INVESTING",
                       "CASH_FLOW_FINANCING"
                   ],
                   bar_mode=bar_mode,
                   color=color,
                   bargap=0.15,
                   bargroupgap=0.1).render()

    if view_type == 'Subplots':
        # Additional logic to create subplots for different metrics
        metrics = [
            "CASH_FLOW_OPERATING", "CASH_FLOW_INVESTING", "CASH_FLOW_FINANCING"
        ]
        for metric in metrics:
            FinancialChart(chart_type="bar",
                           data=df_cash_flow,
                           title=f"{metric} over Time",
                           x_axis="DATE",
                           y_axis=metric,
                           color='ENTITY',
                           bargap=0.15,
                           bargroupgap=0.1).render()


def render_profit_margin_trend_chart(df_profitability):
    FinancialChart(chart_type="line",
                   data=df_profitability,
                   title="Profit Margin Trend",
                   x_axis="DATE",
                   y_axis="PROFIT_MARGIN").render()


def render_current_ratio_trend_chart(df_liquidity):
    FinancialChart(chart_type="line",
                   data=df_liquidity,
                   title="Current Ratio Trend",
                   x_axis="DATE",
                   y_axis="CURRENT_RATIO").render()


# Register charts
register_chart('Assets vs Liabilities', render_assets_vs_liabilities_chart)
register_chart('Debt to Equity Ratio', render_debt_to_equity_chart)
register_chart('Cash Flow Summary', render_cash_flow_summary_chart)
register_chart('Profit Margin Trend', render_profit_margin_trend_chart)
register_chart('Current Ratio Trend', render_current_ratio_trend_chart)
