from app.gallery.components.elements.dashboard.setup import (SecondTierCharts,
                                                             register_chart)


def render_yoy_growth_cash_flow_chart(df_yoy_growth, column):
    SecondTierCharts(chart_type="line",
                     data=df_yoy_growth,
                     title=f'Year-over-Year Growth: {column}',
                     x_axis="DATE",
                     y_axis=column,
                     labels={
                         column: 'Growth (%)'
                     }).render()


def render_net_cash_flow_chart(df_net_flow):
    SecondTierCharts(chart_type="bar",
                     data=df_net_flow,
                     title="Net Cash Flow Over Time",
                     color='ENTITY',
                     labels={
                         'Net_Cash_Flow': 'Net Cash Flow'
                     },
                     x_axis="DATE",
                     y_axis='Net_Cash_Flow').render()


def render_comparative_analysis_cash_flow_chart(filtered_data,
                                                selected_metrics):
    SecondTierCharts(chart_type="line",
                     data=filtered_data,
                     title="Comparative Analysis Over Time",
                     x_axis="DATE",
                     y_axis=selected_metrics,
                     labels={
                         metric: metric.replace('_', ' ').title()
                         for metric in selected_metrics
                     }).render(use_container_width=True)


register_chart('Comparative Analysis Over Time',
               render_comparative_analysis_cash_flow_chart)
register_chart('Net Cash Flow Over Time', render_net_cash_flow_chart)
register_chart('Year-over-Year Growth', render_yoy_growth_cash_flow_chart)
register_chart('Year-over-Year Cash Flow Growth',
               render_yoy_growth_cash_flow_chart)
