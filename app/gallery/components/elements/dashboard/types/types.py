ASSETS_LIABILITIES_CARD_CONTENT = (
    "This card offers an overview of the financial health of the entity by examining its current assets, "
    "current liabilities, and current ratio. Current assets and liabilities provide insights into the entity's "
    "liquidity, while the current ratio measures its ability to meet short-term obligations. Understanding "
    "these metrics helps assess the entity's short-term financial stability.")

CASH_FLOW_CARD_CONTENT = (
    "This card focuses on the entity's cash flow activities, including cash flows from operating, investing, "
    "and financing activities. Operating cash flow reflects the cash generated from core business operations, "
    "while investing and financing cash flows represent investment and financing activities. Analyzing these "
    "cash flow components provides valuable insights into the entity's cash management and financial strategies."
)

LIQUIDITY_CARD_CONTENT = (
    "This card highlights the entity's financial position by examining its current assets, current liabilities, "
    "stockholders' equity, asset-to-liability ratio, and debt-to-equity ratio. These metrics help assess the "
    "entity's overall financial strength, liquidity, and leverage. Understanding the entity's financial position "
    "is crucial for investors and stakeholders to make informed decisions.")

PROFITABILITY_CARD_CONTENT = (
    "This card provides insights into the profitability of the entity over a specific period."
    "It includes key financial metrics such as revenue, net income, operating income, "
    "and profit margin percentage. These metrics offer a comprehensive view of the entity's "
    "financial performance and its ability to generate profits from its operations."
)

# TODO: replace keys in bar chart with below mapping
# TODO: strip '..Value' off bar chart's legend
query_keys_mapping = {
    "Assets Liability": [
        "ASSETS_CURRENTValue", "LIABILITIES_CURRENTValue",
        "STOCKHOLDERS_EQUITYValue"
    ],
    "Cash Flow": [
        "CASH_FLOW_FINANCINGValue", "CASH_FLOW_INVESTINGValue",
        "CASH_FLOW_OPERATINGValue"
    ],
    "Liquidity": ["CURRENT_ASSETSValue", "CURRENT_LIABILITIESValue"]
}

ASSETS_LIABILITIES_DEFAULT_COLUMNS = [
    {
        "field": 'year',
        "headerName": 'Year',
        "width": 90
    },
    {
        "field": 'ASSETS_CURRENT',
        "headerName": 'Current Assets',
        "width": 150,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'LIABILITIES_CURRENT',
        "headerName": 'Current Liabilities',
        "width": 180,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'STOCKHOLDERS_EQUITY',
        "headerName": 'Stockholders Equity',
        "width": 180,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'ASSET_TO_LIABILITY_RATIO',
        "headerName": 'Asset to Liability Ratio',
        "width": 220,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'DEBT_TO_EQUITY_RATIO',
        "headerName": 'Debt to Equity Ratio',
        "width": 180,
        "editable": True,
        "type": 'number'
    },
]

CASH_FLOW_DEFAULT_COLUMNS = [
    {
        "field": 'year',
        "headerName": 'Year',
        "width": 90
    },
    {
        "field": 'CASH_FLOW_OPERATING',
        "headerName": 'Operating Cash Flow',
        "width": 200,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'CASH_FLOW_INVESTING',
        "headerName": 'Investing Cash Flow',
        "width": 200,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'CASH_FLOW_FINANCING',
        "headerName": 'Financing Cash Flow',
        "width": 200,
        "editable": True,
        "type": 'number'
    },
]

LIQUIDITY_DEFAULT_COLUMNS = [
    {
        "field": 'year',
        "headerName": 'Year',
        "width": 90
    },
    {
        "field": 'CURRENT_ASSETS',
        "headerName": 'Current Assets',
        "width": 150,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'CURRENT_LIABILITIES',
        "headerName": 'Current Liabilities',
        "width": 180,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'CURRENT_RATIO',
        "headerName": 'Current Ratio',
        "width": 130,
        "editable": True,
        "type": 'number'
    },
]

PROFITABILITY_DEFAULT_COLUMNS = [
    {
        "field": 'year',
        "headerName": 'Year',
        "width": 90
    },
    {
        "field": 'REVENUES',
        "headerName": 'Revenue',
        "width": 150,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'NET_INCOME_LOSS',
        "headerName": 'Net Income',
        "width": 150,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'OPS_INCOME_LOSS',
        "headerName": 'Operating Income',
        "width": 150,
        "editable": True,
        "type": 'number'
    },
    {
        "field": 'PROFIT_MARGIN',
        "headerName": 'Profit Margin%',
        "width": 150,
        "editable": True,
        "type": 'number'
    },
]
