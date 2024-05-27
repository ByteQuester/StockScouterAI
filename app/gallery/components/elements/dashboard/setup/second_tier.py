import plotly.express as px
import streamlit as st


class SecondTierCharts:

    def __init__(self,
                 chart_type,
                 data,
                 title,
                 x_axis,
                 y_axis,
                 color='ENTITY',
                 bar_mode='group',
                 **kwargs):
        """
        Initializes the FinancialChart class with the chart configuration.

        :param chart_type: The type of chart to render (e.g., 'bar', 'line', 'scatter').
        :param data: The DataFrame containing the data to plot.
        :param title: The title of the chart.
        :param x_axis: The column name in 'data' to use for the x-axis.
        :param y_axis: A list of column names in 'data' to use for the y-axis or a single column name.
        :param color: The DataFrame column to use for coloring elements in the chart, defaults to 'ENTITY'.
        :param bar_mode: Mode for the bar chart ('group', 'stack'), applies only when chart_type is 'bar'.
        :param kwargs: Additional keyword arguments to pass to the Plotly Express chart function.
        """
        self.chart_type = chart_type
        self.data = data
        self.title = title
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.color = color
        self.bar_mode = bar_mode
        self.kwargs = kwargs

    def render(self, use_container_width=True):
        # Select the appropriate chart function based on the type
        if self.chart_type == 'bar':
            fig = px.bar(self.data,
                         x=self.x_axis,
                         y=self.y_axis,
                         color=self.color,
                         title=self.title,
                         **self.kwargs)
            fig.update_layout(
                barmode=self.bar_mode)  # Update the bar mode here
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

        # Optional: Update text and color customization
        if 'text' in self.kwargs:
            fig.update_traces(texttemplate=self.kwargs['text'],
                              textposition='top center')
        if 'color_discrete_sequence' in self.kwargs:
            fig.update_traces(
                marker_color=self.kwargs['color_discrete_sequence'])

        # Display the chart in the Streamlit app
        st.plotly_chart(fig, use_container_width=use_container_width)

    def _get_chart_func(self):
        """
        Returns the Plotly Express function corresponding to the specified chart type.
        """
        chart_funcs = {'bar': px.bar, 'line': px.line, 'scatter': px.scatter}
        return chart_funcs.get(
            self.chart_type,
            px.line)  # Default to line chart if type is unknown
