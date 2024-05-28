from .assets_liabilities import ASSETS_LIABILITIES_QUERY_FILES
from .cash_flow import CASH_FLOW_QUERY_FILES
from .liquidity import LIQUIDITY_QUERY_FILES
from .profitability import PROFITABILITY_QUERY_FILES

SQL_QUERY_FILES = {
    "Assets": ASSETS_LIABILITIES_QUERY_FILES,
    "Cash Flow": CASH_FLOW_QUERY_FILES,
    "Liquidity": LIQUIDITY_QUERY_FILES,
    "Profitability": PROFITABILITY_QUERY_FILES,
}

__all__ = ['SQL_QUERY_FILES']
