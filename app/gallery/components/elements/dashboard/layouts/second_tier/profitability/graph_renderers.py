from app.gallery.components.elements.dashboard.setup import \
    SecondTierCharts, register_chart


def render_qoq_growth_chart(df_qoq_growth):
    SecondTierCharts(chart_type="line",
                     data=df_qoq_growth,
                     title="Quarter-over-Quarter Revenue Growth (%)",
                     x_axis="DATE",
                     y_axis="REVENUES_QoQ_Growth").render()


def render_qoq_profit_margin_chart(df_qoq_growth):
    SecondTierCharts(chart_type="line",
                     data=df_qoq_growth,
                     title="Profit Margin Analysis by Quarter (%)",
                     x_axis="DATE",
                     y_axis="PROFIT_MARGIN").render()


def render_expense_ratio_chart(df_expense_ratio):
    SecondTierCharts(chart_type="scatter",
                     data=df_expense_ratio,
                     title="Expense Ratio Over Time (%)",
                     x_axis="DATE",
                     y_axis="Expense_Ratio").render()


def render_revenue_distribution_chart(df_revenue_distribution):
    color_column = 'ENTITY' if 'ENTITY' in df_revenue_distribution.columns else None
    SecondTierCharts(chart_type="bar",
                     data=df_revenue_distribution,
                     title="Revenue Distribution by Quarter",
                     x_axis="Quarter",
                     y_axis="REVENUES",
                     color=color_column).render()


def render_profit_margin_analysis_chart(df_margin_analysis):
    color_column = 'ENTITY' if 'ENTITY' in df_margin_analysis.columns else None
    SecondTierCharts(
        chart_type="bar",
        data=df_margin_analysis,
        title="Profit Margin Analysis by Quarter (%)",
        x_axis="Quarter",
        y_axis="PROFIT_MARGIN",
        color=color_column  # Conditionally set the color column
    ).render()


def render_comparative_analysis_chart(filtered_data, selected_metrics):
    SecondTierCharts(chart_type="line",
                     data=filtered_data,
                     title="Comparative Analysis Over Time",
                     x_axis="DATE",
                     y_axis=selected_metrics).render(use_container_width=True)


# Chart Registration
register_chart('Quarter-over-Quarter Revenue Growth', render_qoq_growth_chart)
register_chart('Profit Margin Analysis by Quarter',
               render_qoq_profit_margin_chart)
register_chart('Expense Ratio Over Time', render_expense_ratio_chart)
register_chart('Revenue Distribution by Quarter',
               render_revenue_distribution_chart)
register_chart('Profit Margin Analysis by Quarter (Bar)',
               render_profit_margin_analysis_chart)
register_chart('Comparative Analysis Over Time',
               render_comparative_analysis_chart)
