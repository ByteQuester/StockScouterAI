from app.services.queries.query_managers.sql_executor import SQLExecutor

if __name__ == "__main__":
    sql_executor = SQLExecutor()

    # Create the profitability_qoq_growth view
    qoq_growth_sql = """
    CREATE VIEW IF NOT EXISTS profitability_qoq_growth AS
    WITH preprocessed_data AS (
        SELECT *,
               LAG(REVENUES, 1) OVER (PARTITION BY Entity ORDER BY DATE) AS Prev_Revenues,
               LAG(OPS_INCOME_LOSS, 1) OVER (PARTITION BY Entity ORDER BY DATE) AS Prev_OperatingIncomeLoss
        FROM raw_profitability
    )
    SELECT
        Entity,
        CIK,
        DATE,
        Year,
        Quarter,
        NET_INCOME_LOSS,
        REVENUES,
        OPS_INCOME_LOSS,
        PROFIT_MARGIN,
        CASE WHEN Prev_Revenues IS NOT NULL AND Prev_Revenues != 0 THEN
            ROUND ((REVENUES - Prev_Revenues) / Prev_Revenues * 100, 2)
            ELSE NULL END AS Revenues_QoQ_Growth,
        CASE WHEN Prev_OperatingIncomeLoss IS NOT NULL AND Prev_OperatingIncomeLoss != 0 THEN
            ROUND ((OPS_INCOME_LOSS - Prev_OperatingIncomeLoss) / Prev_OperatingIncomeLoss * 100, 2)
            ELSE NULL END AS OperatingIncome_QoQ_Growth
    FROM preprocessed_data;
    """
    sql_executor.execute_sql(qoq_growth_sql)

    # Create the profitability_expense_ratio view
    expense_ratio_sql = """
    CREATE VIEW IF NOT EXISTS profitability_expense_ratio AS
    SELECT *,
           ROUND ((REVENUES - OPS_INCOME_LOSS) / REVENUES * 100, 2) AS Expense_Ratio
    FROM raw_profitability;
    """
    sql_executor.execute_sql(expense_ratio_sql)

    # Create the profitability_analysis view
    analysis_sql = """
    CREATE VIEW IF NOT EXISTS profitability_analysis AS
    SELECT a.Entity,
           a.CIK,
           a.DATE,
           a.Year,
           a.Quarter,
           a.NET_INCOME_LOSS,
           a.REVENUES,
           a.OPS_INCOME_LOSS,
           a.PROFIT_MARGIN,
           b.Revenues_QoQ_Growth,
           b.OperatingIncome_QoQ_Growth,
           c.Expense_Ratio,
           a.REVENUES - a.OPS_INCOME_LOSS AS Operational_Expenses
    FROM raw_profitability a
    LEFT JOIN profitability_qoq_growth b ON a.CIK = b.CIK AND a.DATE = b.DATE
    LEFT JOIN profitability_expense_ratio c ON a.CIK = c.CIK AND a.DATE = c.DATE;
    """
    sql_executor.execute_sql(analysis_sql)

    # Query the profitability_analysis view
    query_sql = "SELECT * FROM profitability_analysis WHERE CIK = ? AND DATE BETWEEN ? AND ?"
    params = ('0000816761', '2020-01-01', '2023-01-01')
    results = sql_executor.query_sql(query_sql, params)
    print("Query results:", results)
