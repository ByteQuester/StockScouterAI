from .assets_liabilities_ import AssetsLiabilityQuery
from .cash_flow_ import CashFlowQuery
from .liquidity_ import LiquidityQuery
from .profitability_ import ProfitabilityQuery

ASSET_LIABILITIES = AssetsLiabilityQuery
CASH_FLOW = CashFlowQuery
# Place-holder for DEBT_MANAGEMENT =
LIQUIDITY = LiquidityQuery
# Place-holder for MARKET_VALUATION
PROFITABILITY = ProfitabilityQuery
# Place-holder for OPERATIONAL_EFFICIENCY

__all__ = ['ASSET_LIABILITIES', 'CASH_FLOW', 'LIQUIDITY', 'PROFITABILITY']
