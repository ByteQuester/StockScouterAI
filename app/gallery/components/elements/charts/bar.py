import json

from streamlit_elements import mui, nivo

from .dashboard import Dashboard


class Bar(Dashboard.Item):
    DEFAULT_DATA = [
        {
            "Date": "2021-06",
            "ProfitMarginPercentValue": 1000,
            "ProfitMarginPercentColor": "hsl(126, 70%, 50%)"
        },
        {
            "Date": "2021-09",
            "ProfitMarginPercentValue": 1100,
            "ProfitMarginPercentColor": "hsl(126, 70%, 50%)"
        },
        {
            "Date": "2021-12",
            "ProfitMarginPercentValue": 1900,
            "ProfitMarginPercentColor": "hsl(126, 70%, 50%)"
        },
        {
            "Date": "2022-03",
            "ProfitMarginPercentValue": 1200,
            "ProfitMarginPercentColor": "hsl(126, 70%, 50%)"
        },
    ]

    def __init__(self, *args, keys=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = keys if keys else ["ProfitMarginPercentValue"]
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

    def __call__(self, json_data):
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
                mui.icon.BarChart()
                mui.Typography("Bar Chart", sx={"flex": 1})

            with mui.Box(sx={'flex': 1, 'minHeight': 0}):
                nivo.Bar(
                    data=data,
                    keys=self.keys,
                    indexBy='Date',
                    margin={
                        'top': 50,
                        'right': 130,
                        'bottom': 50,
                        'left': 60
                    },
                    padding={'0.3'},
                    theme=self._theme['dark' if self._dark_mode else 'light'],
                    valueScale={'type': 'symlog'},
                    indexScale={
                        'type': 'band',
                        'round': True
                    },
                    colors={'scheme': 'nivo'},
                    borderColor={
                        'from': 'color',
                        'modifiers': [['darker', 1.6]]
                    },
                    axisTop=None,
                    axisRight=None,
                    axisBottom={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 45,
                        'legend': 'Date',
                        'legendPosition': 'middle',
                        'legendOffset': 45
                    },
                    axisLeft={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': 'Value',
                        'legendPosition': 'middle',
                        'legendOffset': -40
                    },
                    labelSkipWidth=12,
                    labelSkipHeight=12,
                    labelTextColor={
                        'from': 'color',
                        'modifiers': [['darker', 1.6]]
                    },
                    legends=[{
                        'dataFrom':
                        'keys',
                        'anchor':
                        'bottom-right',
                        'direction':
                        'column',
                        'justify':
                        False,
                        'translateX':
                        90,
                        'translateY':
                        0,
                        'itemsSpacing':
                        2,
                        'itemWidth':
                        100,
                        'itemHeight':
                        20,
                        'itemDirection':
                        'left-to-right',
                        'itemOpacity':
                        0.85,
                        'symbolSize':
                        20,
                        'effects': [{
                            'on': 'hover',
                            'style': {
                                'itemOpacity': 5
                            }
                        }]
                    }],
                    role='application',
                    ariaLabel='Nivo bar chart',
                )
