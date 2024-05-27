from app.gallery.components.elements.dashboard.setup import \
    SecondTierCharts, register_chart


def render_qoq_growth_liquidity_chart(df_qoq_growth):
    SecondTierCharts(chart_type="line",
                     data=df_qoq_growth,
                     title="Quarter-over-Quarter Growth of Current Assets (%)",
                     x_axis="DATE",
                     y_axis="CURRENT_ASSETS_QoQ_Growth").render()


def render_current_ratio_chart(filtered_data):
    SecondTierCharts(chart_type="line",
                     data=filtered_data,
                     title="Current Ratio Over Time",
                     x_axis="DATE",
                     y_axis="CURRENT_RATIO").render()


def render_comparative_analysis_liquidity_chart(filtered_data,
                                                selected_metrics):
    SecondTierCharts(chart_type="line",
                     data=filtered_data,
                     title="Comparative Analysis Over Time",
                     x_axis="DATE",
                     y_axis=selected_metrics).render(use_container_width=True)


register_chart('Comparative Analysis Over Time',
               render_comparative_analysis_liquidity_chart)
register_chart('Current Ratio Over Time', render_current_ratio_chart)
register_chart('Quarter-over-Quarter Growth of Current Assets',
               render_qoq_growth_liquidity_chart)
