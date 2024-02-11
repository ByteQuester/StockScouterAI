# queries/sql_tables/__init__.py

SQL_QUERY_FILES = {
    "Assets Liabilities":
    "app/services/queries/sql_tables/assets_liabilities_query.sql",
    "Cash Flow": "app/services/queries/sql_tables/cash_flow_query.sql",
    "Debt Management":
    "app/services/queries/sql_tables/debt_management_query.sql",
    "Liquidity": "app/services/queries/sql_tables/liquidity_query.sql",
    "Market Valuation":
    "app/services/queries/sql_tables/market_valuation_query.sql",
    "Operational Efficiency":
    "app/services/queries/sql_tables/operational_efficiency_query.sql",
    "Profitability": "app/services/queries/sql_tables/profitability_query.sql"
}

__all__ = ['SQL_QUERY_FILES']
