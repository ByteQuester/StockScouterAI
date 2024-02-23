from enum import Enum


class ChartMetrics(Enum):
    """
    The `ChartMetrics` enum guides the selection of financial metrics for transformation in
    `.functions.transformers.transformers_base.py`, such as "NET_INCOME_LOSS", "REVENUES", and "OPS_INCOME_LOSS".
    To ensure accurate data sets for analysis and visualization:

    1. Review processed data in `.data/{cik}/processed_data` to identify available metrics.
    2. Cross-check these metrics with those listed in `ChartMetrics` to spot any discrepancies.
    3. Update `ChartMetrics` or data as needed to ensure alignment between processed data and visualization requirements.

    """
    ASSETS_LIABILITIES_LINE = [
        "ASSET_TO_LIABILITY_RATIO", "DEBT_TO_EQUITY_RATIO"
    ]
    ASSETS_LIABILITIES_DEBT_LINE = ["ASSET_TO_LIABILITY_RATIO"]
    ASSETS_LIABILITIES_EQUITY_LINE = ["DEBT_TO_EQUITY_RATIO"]
    ASSETS_LIABILITIES_BAR = [
        "ASSETS_CURRENT", "LIABILITIES_CURRENT", "STOCKHOLDERS_EQUITY"
    ]
    CASH_FLOW = [
        "CASH_FLOW_FINANCING", "CASH_FLOW_INVESTING", "CASH_FLOW_OPERATING"
    ]
    LIQUIDITY_LINE = ["CURRENT_RATIO"]
    LIQUIDITY_BAR = ["CURRENT_ASSETS", "CURRENT_LIABILITIES"]
    PROFITABILITY_LINE = ["NET_INCOME_LOSS", "REVENUES", "OPS_INCOME_LOSS"]
    PROFITABILITY_MARGIN_LINE = ["PROFIT_MARGIN"]
