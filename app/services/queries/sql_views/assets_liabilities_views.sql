-- Create a view for calculating quarter-over-quarter growth
CREATE VIEW IF NOT EXISTS assets_liabilities_qoq_growth AS
WITH preprocessed_data AS (
    SELECT *,
           LAG(ASSETS_CURRENT, 1) OVER (PARTITION BY ENTITY ORDER BY DATE) AS Prev_ASSETS_CURRENT,
           LAG(LIABILITIES_CURRENT, 1) OVER (PARTITION BY ENTITY ORDER BY DATE) AS Prev_LIABILITIES_CURRENT
    FROM raw_assets_liabilities
)
SELECT
    ENTITY,
    CIK,
    DATE,
    Year,
    Quarter,
    ASSETS_CURRENT,
    LIABILITIES_CURRENT,
    STOCKHOLDERS_EQUITY,
    ASSET_TO_LIABILITY_RATIO,
    DEBT_TO_EQUITY_RATIO,
    CASE WHEN Prev_ASSETS_CURRENT IS NOT NULL THEN
        ROUND((ASSETS_CURRENT - Prev_ASSETS_CURRENT) / Prev_ASSETS_CURRENT * 100, 2)
        ELSE NULL END AS ASSETS_CURRENT_QoQ_Growth,
    CASE WHEN Prev_LIABILITIES_CURRENT IS NOT NULL THEN
        ROUND((LIABILITIES_CURRENT - Prev_LIABILITIES_CURRENT) / Prev_LIABILITIES_CURRENT * 100, 2)
        ELSE NULL END AS LIABILITIES_CURRENT_QoQ_Growth
FROM preprocessed_data;

-- Create a view for calculating working capital
CREATE VIEW IF NOT EXISTS assets_liabilities_working_capital AS
SELECT *,
       ROUND(ASSETS_CURRENT - LIABILITIES_CURRENT, 2) AS Working_Capital
FROM raw_assets_liabilities;

-- Combine all calculations into a single view
CREATE VIEW IF NOT EXISTS assets_liabilities_analysis AS
SELECT a.ENTITY,
       a.CIK,
       a.DATE,
       a.Year,
       a.Quarter,
       a.ASSETS_CURRENT,
       a.LIABILITIES_CURRENT,
       a.STOCKHOLDERS_EQUITY,
       a.ASSET_TO_LIABILITY_RATIO,
       a.DEBT_TO_EQUITY_RATIO,
       b.ASSETS_CURRENT_QoQ_Growth,
       b.LIABILITIES_CURRENT_QoQ_Growth,
       c.Working_Capital
FROM raw_assets_liabilities a
LEFT JOIN assets_liabilities_qoq_growth b ON a.CIK = b.CIK AND a.DATE = b.DATE
LEFT JOIN assets_liabilities_working_capital c ON a.CIK = c.CIK AND a.DATE = c.DATE;
