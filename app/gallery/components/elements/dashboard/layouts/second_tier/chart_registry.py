# chart_registry.py

chart_registry = {}


def register_chart(name, render_func):
    """
    Register a chart with a name and a rendering function.
    :param name: The name of the chart.
    :param render_func: The function that renders the chart.
    """
    chart_registry[name] = render_func


def render_chart(name, *args, **kwargs):
    """
    Render a registered chart.
    :param name: The name of the registered chart.
    :param args: Positional arguments for the render function.
    :param kwargs: Keyword arguments for the render function.
    """
    if name in chart_registry:
        chart_registry[name](*args, **kwargs)
    else:
        raise ValueError(f"Chart '{name}' is not registered.")
