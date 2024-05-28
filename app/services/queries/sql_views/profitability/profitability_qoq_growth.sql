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
