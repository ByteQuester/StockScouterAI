from .category_metrics import CategoryMetrics
from .chart_metrics import ChartMetrics
from .file_paths import FilePaths
from .metrics import AnnualMetrics, QuarterlyMetrics
from .query_folder_mapping import QueryFolderMapping
from .sec_endpoints import SECEndpoints

ANNUAL_METRICS = [metric.value for metric in AnnualMetrics]
QUARTERLY_METRICS = [metric.value for metric in QuarterlyMetrics]

ASSET_LIABILITIES_METRICS = CategoryMetrics.ASSETS_LIABILITIES.value
CASH_FLOW_METRICS = CategoryMetrics.CASH_FLOW.value
LIQUIDITY_METRICS = CategoryMetrics.LIQUIDITY.value
PROFITABILITY_METRICS = CategoryMetrics.PROFITABILITY.value

BASE_URL = SECEndpoints.BASE_URL.value
COMPANY_TICKERS = SECEndpoints.COMPANY_TICKERS.value
SUBMISSIONS = SECEndpoints.SUBMISSIONS.value
COMPANY_FACTS = SECEndpoints.COMPANY_FACTS.value

ASSETS_LIABILITIES_BAR_METRICS = ChartMetrics.ASSETS_LIABILITIES_BAR
ASSETS_LIABILITIES_DEBT_LINE_METRIC = ChartMetrics.ASSETS_LIABILITIES_DEBT_LINE
ASSETS_LIABILITIES_EQUITY_LINE_METRIC = ChartMetrics.ASSETS_LIABILITIES_EQUITY_LINE
ASSETS_LIABILITIES_LINE_METRICS = ChartMetrics.ASSETS_LIABILITIES_LINE

CASH_FLOW_CHARTS_METRICS = ChartMetrics.CASH_FLOW
LIQUIDITY_LINE_METRICS = ChartMetrics.LIQUIDITY_LINE
LIQUIDITY_BAR_METRICS = ChartMetrics.LIQUIDITY_BAR
PROFITABILITY_LINE_METRICS = ChartMetrics.PROFITABILITY_LINE
PROFITABILITY_MARGIN_LINE_METRIC = ChartMetrics.PROFITABILITY_MARGIN_LINE

DEFAULT_STAGE_NAME = FilePaths().DEFAULT_STAGE_NAME
DEFAULT_TABLE_NAME = FilePaths().DEFAULT_TABLE_NAME
CSV_DIRECTORY = FilePaths().CSV_DIRECTORY
CSV_FILE_PATH = FilePaths().CSV_FILE_PATH

__all__ = [
    'ANNUAL_METRICS', 'ASSETS_LIABILITIES_BAR_METRICS',
    'ASSETS_LIABILITIES_DEBT_LINE_METRIC',
    'ASSETS_LIABILITIES_EQUITY_LINE_METRIC', 'ASSETS_LIABILITIES_LINE_METRICS',
    'ASSET_LIABILITIES_METRICS', 'BASE_URL', 'CASH_FLOW_METRICS',
    'CASH_FLOW_CHARTS_METRICS', 'COMPANY_FACTS', 'COMPANY_TICKERS',
    'CSV_DIRECTORY', 'CSV_FILE_PATH', 'DEFAULT_STAGE_NAME',
    'DEFAULT_TABLE_NAME', 'FilePaths', 'LIQUIDITY_BAR_METRICS',
    'LIQUIDITY_LINE_METRICS', 'LIQUIDITY_METRICS',
    'PROFITABILITY_LINE_METRICS', 'PROFITABILITY_MARGIN_LINE_METRIC',
    'PROFITABILITY_METRICS', 'QUARTERLY_METRICS', 'QueryFolderMapping',
    'SECEndpoints', 'SUBMISSIONS'
]
