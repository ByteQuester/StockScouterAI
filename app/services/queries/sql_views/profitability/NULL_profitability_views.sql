-- Create a view for calculating quarter-over-quarter growth
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

-- Create a view for calculating the expense ratio
CREATE VIEW IF NOT EXISTS profitability_expense_ratio AS
SELECT *,
       ROUND ((REVENUES - OPS_INCOME_LOSS) / REVENUES * 100, 2) AS Expense_Ratio
FROM raw_profitability;

-- Combine all calculations into a single view
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
