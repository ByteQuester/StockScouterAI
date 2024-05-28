from app.gallery.components.elements.dashboard.setup import (SecondTierCharts,
                                                             register_chart)


def render_qoq_growth_assets_chart(df_qoq_growth):
    SecondTierCharts(chart_type="line",
                     data=df_qoq_growth,
                     title="Quarter-over-Quarter Growth of Current Assets (%)",
                     x_axis="DATE",
                     y_axis="ASSETS_CURRENT_QoQ_Growth").render()


def render_working_capital_chart(df_working_capital):
    SecondTierCharts(chart_type="line",
                     data=df_working_capital,
                     title="Working Capital Over Time",
                     x_axis="DATE",
                     y_axis="Working_Capital").render()


def render_asset_liability_ratio_chart(filtered_data):
    SecondTierCharts(chart_type="line",
                     data=filtered_data,
                     title="Asset To Liability Ratio Over Time",
                     x_axis="DATE",
                     y_axis="ASSET_TO_LIABILITY_RATIO").render()


def render_debt_equity_ratio_chart(filtered_data):
    SecondTierCharts(chart_type="line",
                     data=filtered_data,
                     title="Debt to Equity Ratio Over Time",
                     x_axis="DATE",
                     y_axis="DEBT_TO_EQUITY_RATIO").render()


def render_comparative_analysis_assets_chart(filtered_data, selected_metrics):
    SecondTierCharts(chart_type="line",
                     data=filtered_data,
                     title="Comparative Analysis Over Time",
                     x_axis="DATE",
                     y_axis=selected_metrics).render(use_container_width=True)


register_chart('Comparative Analysis Over Time',
               render_comparative_analysis_assets_chart)
register_chart('Debt to Equity Ratio Over Time',
               render_debt_equity_ratio_chart)
register_chart('Asset To Liability Ratio Over Time',
               render_asset_liability_ratio_chart)
register_chart('Quarter-over-Quarter Growth of Current Assets',
               render_qoq_growth_assets_chart)
register_chart('Working Capital Over Time', render_working_capital_chart)
