-- Create a view for calculating quarter-over-quarter growth
CREATE VIEW IF NOT EXISTS liquidity_qoq_growth AS
WITH preprocessed_data AS (
    SELECT *,
           LAG(CURRENT_ASSETS, 1) OVER (PARTITION BY Entity ORDER BY DATE) AS Prev_CURRENT_ASSETS,
           LAG(CURRENT_LIABILITIES, 1) OVER (PARTITION BY Entity ORDER BY DATE) AS Prev_CURRENT_LIABILITIES
    FROM raw_liquidity
)
SELECT
    Entity,
    CIK,
    DATE,
    Year,
    Quarter,
    CURRENT_ASSETS,
    CURRENT_LIABILITIES,
    CURRENT_RATIO,
    CASE WHEN Prev_CURRENT_ASSETS IS NOT NULL THEN
        ROUND((CURRENT_ASSETS - Prev_CURRENT_ASSETS) / Prev_CURRENT_ASSETS * 100, 2)
        ELSE NULL END AS CURRENT_ASSETS_QoQ_Growth,
    CASE WHEN Prev_CURRENT_LIABILITIES IS NOT NULL THEN
        ROUND((CURRENT_LIABILITIES - Prev_CURRENT_LIABILITIES) / Prev_CURRENT_LIABILITIES * 100, 2)
        ELSE NULL END AS CURRENT_LIABILITIES_QoQ_Growth
FROM preprocessed_data;

-- Combine all calculations into a single view
CREATE VIEW IF NOT EXISTS liquidity_analysis AS
SELECT a.Entity,
       a.CIK,
       a.DATE,
       a.Year,
       a.Quarter,
       a.CURRENT_ASSETS,
       a.CURRENT_LIABILITIES,
       a.CURRENT_RATIO,
       b.CURRENT_ASSETS_QoQ_Growth,
       b.CURRENT_LIABILITIES_QoQ_Growth
FROM raw_liquidity a
LEFT JOIN liquidity_qoq_growth b ON a.CIK = b.CIK AND a.DATE = b.DATE;
