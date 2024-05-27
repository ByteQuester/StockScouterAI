import plotly.express as px
import streamlit as st


class GeneralTierChart:

    def __init__(self,
                 chart_type,
                 data,
                 title,
                 x_axis,
                 y_axis,
                 color='ENTITY',
                 bar_mode='group',
                 bargap=0.1,
                 bargroupgap=0.0,
                 **kwargs):
        """
        Initializes the FinancialChart class with the chart configuration.

        :param chart_type: The type of chart to render (e.g., 'bar', 'line', 'scatter').
        :param data: The DataFrame containing the data to plot.
        :param title: The title of the chart.
        :param x_axis: The column name in 'data' to use for the x-axis.
        :param y_axis: A list of column names in 'data' to use for the y-axis or a single column name.
        :param color: The DataFrame column to use for coloring elements in the chart, defaults to 'CIK'.
        :param bar_mode: Mode for the bar chart ('group', 'stack'), applies only when chart_type is 'bar'.
        :param bargap: Gap between bars (0 to 1), default is 0.1.
        :param bargroupgap: Gap between groups of bars (0 to 1), default is 0.0.
        :param kwargs: Additional keyword arguments to pass to the Plotly Express chart function.
        """
        self.chart_type = chart_type
        self.data = data
        self.title = title
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.color = color
        self.bar_mode = bar_mode
        self.bargap = bargap
        self.bargroupgap = bargroupgap
        self.kwargs = kwargs

    def render(self, use_container_width=True):
        if self.chart_type == 'bar':
            if isinstance(self.y_axis, list) and self.color:
                melted_data = self.data.melt(id_vars=[self.x_axis, self.color],
                                             value_vars=self.y_axis,
                                             var_name='Metric',
                                             value_name='Value')
                fig = px.bar(melted_data,
                             x=self.x_axis,
                             y='Value',
                             color=self.color,
                             pattern_shape='Metric',
                             title=self.title,
                             **self.kwargs)
                fig.update_layout(barmode=self.bar_mode,
                                  bargap=self.bargap,
                                  bargroupgap=self.bargroupgap)
            else:
                fig = px.bar(self.data,
                             x=self.x_axis,
                             y=self.y_axis,
                             color=self.color,
                             title=self.title,
                             **self.kwargs)
                fig.update_layout(barmode=self.bar_mode,
                                  bargap=self.bargap,
                                  bargroupgap=self.bargroupgap)
        elif self.chart_type == 'line':
            fig = px.line(self.data,
                          x=self.x_axis,
                          y=self.y_axis,
                          color=self.color,
                          title=self.title,
                          **self.kwargs)
        elif self.chart_type == 'scatter':
            fig = px.scatter(self.data,
                             x=self.x_axis,
                             y=self.y_axis,
                             color=self.color,
                             title=self.title,
                             **self.kwargs)

        st.plotly_chart(fig, use_container_width=use_container_width)

    def _get_chart_func(self):
        chart_funcs = {'bar': px.bar, 'line': px.line, 'scatter': px.scatter}
        return chart_funcs.get(self.chart_type, px.line)
