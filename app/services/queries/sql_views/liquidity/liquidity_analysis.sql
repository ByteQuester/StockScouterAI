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
