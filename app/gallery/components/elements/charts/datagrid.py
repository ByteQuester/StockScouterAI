import json

from streamlit_elements import mui

from .dashboard import Dashboard


class DataGrid(Dashboard.Item):

    DEFAULT_COLUMNS = [
        {
            "field": 'year',
            "headerName": 'Year',
            "width": 90
        },
        {
            "field": 'revenue',
            "headerName": 'Revenue',
            "width": 150,
            "editable": True,
            "type": 'number'
        },
        {
            "field": 'netIncome',
            "headerName": 'Net Income',
            "width": 150,
            "editable": True,
            "type": 'number'
        },
        {
            "field": 'operatingIncome',
            "headerName": 'Operating Income',
            "width": 150,
            "editable": True,
            "type": 'number'
        },
        {
            "field": 'profitMargin',
            "headerName": 'Profit Margin%',
            "width": 150,
            "editable": True,
            "type": 'number'
        },
    ]
    DEFAULT_ROWS = [
        {
            "id": 1,
            "year": "2008-06",
            "revenue": 16962.0,
            "netIncome": 852.0,
            "operatingIncome": 1247.0,
            "profitMargin": 1.2
        },
        {
            "id": 2,
            "year": "2008-09",
            "revenue": 15293.0,
            "netIncome": 695.0,
            "operatingIncome": 1147.0,
            "profitMargin": 0.2
        },
        {
            "id": 3,
            "year": "2009-03",
            "revenue": 16502.0,
            "netIncome": 610.0,
            "operatingIncome": 1025.0,
            "profitMargin": -1.2
        },
        {
            "id": 4,
            "year": "2009-06",
            "revenue": 17154.0,
            "netIncome": 998.0,
            "operatingIncome": 1529.0,
            "profitMargin": -0.8
        },
        {
            "id": 5,
            "year": "2009-09",
            "revenue": 16688.0,
            "netIncome": -1564.0,
            "operatingIncome": -2151.0,
            "profitMargin": 0
        },
    ]

    def __init__(self, *args, columns=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns = columns if columns else self.DEFAULT_COLUMNS

    def _handle_edit(self, params):
        print(params)

    def __call__(self, json_data):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = self.DEFAULT_ROWS

        with mui.Paper(key=self._key,
                       sx={
                           "display": "flex",
                           "flexDirection": "column",
                           "borderRadius": 3,
                           "overflow": "hidden"
                       },
                       elevation=1):
            with self.title_bar(padding="10px 15px 10px 15px",
                                dark_switcher=False):
                mui.icon.ViewCompact()
                mui.Typography("Data grid")

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                mui.DataGrid(
                    columns=self.columns,
                    rows=data,
                    pageSize=5,
                    rowsPerPageOptions=[5],
                    checkboxSelection=True,
                    disableSelectionOnClick=True,
                    onCellEditCommit=self._handle_edit,
                )
