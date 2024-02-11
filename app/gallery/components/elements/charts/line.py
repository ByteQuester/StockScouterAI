import json

import yaml
from streamlit_elements import mui, nivo

from .dashboard import Dashboard


class Line(Dashboard.Item):
    DEFAULT_DATA = [{
        "id":
        "NetIncomeLoss",
        "data": [
            {
                "x": "2008-06",
                "y": 852.0
            },
            {
                "x": "2008-09",
                "y": 695.0
            },
            {
                "x": "2009-03",
                "y": 610.0
            },
            {
                "x": "2009-06",
                "y": 998.0
            },
            {
                "x": "2009-09",
                "y": -1564.0
            },
        ]
    }, {
        "id":
        "Revenues",
        "data": [
            {
                "x": "2008-06",
                "y": 16962.0
            },
            {
                "x": "2008-09",
                "y": 15293.0
            },
            {
                "x": "2009-03",
                "y": 16502.0
            },
            {
                "x": "2009-06",
                "y": 17154.0
            },
            {
                "x": "2009-09",
                "y": 16688.0
            },
        ]
    }, {
        "id":
        "OperatingIncomeLoss",
        "data": [
            {
                "x": "2008-06",
                "y": 1247.0
            },
            {
                "x": "2008-09",
                "y": 1147.0
            },
            {
                "x": "2009-03",
                "y": 1025.0
            },
            {
                "x": "2009-06",
                "y": 1529.0
            },
            {
                "x": "2009-09",
                "y": -2151.0
            },
        ]
    }]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._theme = {
            "dark": {
                "background": "#252526",
                "textColor": "#FAFAFA",
                "tooltip": {
                    "container": {
                        "background": "#3F3F3F",
                        "color": "FAFAFA",
                    }
                }
            },
            "light": {
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        }

    def __call__(self, json_data, config_type='base_config'):
        with open('app/gallery/configs/line_chart.yml', 'r') as file:
            configs = yaml.safe_load(file)
        config = configs[config_type]
        theme_key = "dark" if self._dark_mode else "light"
        config['theme'] = self._theme[theme_key]
        """ignore warning to allow flexibility in how the __call__ method is implemented across different subclasses."""
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = self.DEFAULT_DATA

        with mui.Paper(key=self._key,
                       sx={
                           "display": "flex",
                           "flexDirection": "column",
                           "borderRadius": 3,
                           "overflow": "hidden"
                       },
                       elevation=1):
            with self.title_bar():
                mui.icon.ShowChart()
                mui.Typography("Line Chart", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.Line(data=data, **config)
