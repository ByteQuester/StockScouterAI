from enum import Enum


class CategoryMetrics(Enum):
    """
    CategoryMetrics groups metrics by analysis category. This categorization is used throughout the project
    to direct the data through appropriate preprocessing, processing, and transformation pipelines based on the
    category of analysis, ensuring data is stored and processed in its respective context (e.g., folders)."""
    ASSETS_LIABILITIES = [
        'AssetsCurrent', 'LiabilitiesCurrent', 'StockholdersEquity'
    ]
    CASH_FLOW = [
        'NetCashProvidedByUsedInOperatingActivities',
        'NetCashProvidedByUsedInInvestingActivities',
        'NetCashProvidedByUsedInFinancingActivities'
    ]
    LIQUIDITY = ['AssetsCurrent', 'LiabilitiesCurrent']
    #DEV
    PROFITABILITY = [
        'OperatingIncomeLoss',
        'RevenueFromContractWithCustomerExcludingAssessedTax', 'NetIncomeLoss'
    ]

    @classmethod
    def get_metrics(cls, category):
        return cls[category].value if category in cls.__members__ else None
