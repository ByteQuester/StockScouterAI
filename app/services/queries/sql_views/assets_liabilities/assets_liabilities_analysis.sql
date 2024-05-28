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
