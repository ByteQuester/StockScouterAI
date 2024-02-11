from enum import Enum


class AnnualMetrics(Enum):
    """ AnnualMetrics and QuarterlyMetrics encapsulate metrics directly available from SEC endpoints.
     The distinction between annual and quarterly metrics is crucial as they are available in their respective fields
     within the SEC data, ensuring the correct temporal scope is applied during analysis."""
    ASSETS = "Assets"
    CAPITAL_EXPENDITURES = "CapitalExpendituresIncurredButNotYetPaid"
    OPERATING_CASH_FLOW = "NetCashProvidedByUsedInOperatingActivities"
    INVESTING_CASH_FLOW = "NetCashProvidedByUsedInInvestingActivities"
    FINANCING_CASH_FLOW = "NetCashProvidedByUsedInFinancingActivities"


class QuarterlyMetrics(Enum):
    STOCKHOLDERS_EQUITY = "StockholdersEquity"
    ASSETS_CURRENT = "AssetsCurrent"
    LIABILITIES_CURRENT = "LiabilitiesCurrent"
    OPERATING_INCOME_LOSS = "OperatingIncomeLoss"
    REVENUES = "Revenues"
    NET_INCOME_LOSS = "NetIncomeLoss"


# Utility function to simplify access to all metrics
def all_metrics():
    annual = [metric.value for metric in AnnualMetrics]
    quarterly = [metric.value for metric in QuarterlyMetrics]
    return annual + quarterly
