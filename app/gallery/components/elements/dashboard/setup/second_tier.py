import plotly.express as px
import streamlit as st


class FinancialChart:

    def __init__(self, chart_type, data, title, x_axis, y_axis, **kwargs):
        """
        Initializes the FinancialChart class with the chart configuration.

        :param chart_type: The type of chart to render (e.g., 'bar', 'line').
        :param data: The DataFrame containing the data to plot.
        :param title: The title of the chart.
        :param x_axis: The column name in 'data' to use for the x-axis.
        :param y_axis: A list of column names in 'data' to use for the y-axis or a single column name.
        :param kwargs: Additional keyword arguments to pass to the Plotly Express chart function.
        """
        self.chart_type = chart_type
        self.data = data
        self.title = title
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.kwargs = kwargs

    def render(self, use_container_width=False):
        chart_func = self._get_chart_func()
        fig = chart_func(data_frame=self.data,
                         x=self.x_axis,
                         y=self.y_axis,
                         title=self.title,
                         **self.kwargs)
        # Check if text/annotations should be added
        if 'text' in self.kwargs:
            fig.update_traces(texttemplate=self.kwargs['text'],
                              textposition='top center')

        # Check for color palette customization
        if 'color_discrete_sequence' in self.kwargs:
            fig.update_traces(
                marker_color=self.kwargs['color_discrete_sequence'])

        st.plotly_chart(fig, use_container_width=use_container_width)

    def _get_chart_func(self):
        """
        Returns the Plotly Express function corresponding to the specified chart type.
        """
        chart_funcs = {
            'bar': px.bar,
            'line': px.line,
            'scatter': px.scatter
            # Add mappings for additional chart types as needed
        }
        return chart_funcs.get(
            self.chart_type,
            px.line)  # Default to line chart if type is unknown
