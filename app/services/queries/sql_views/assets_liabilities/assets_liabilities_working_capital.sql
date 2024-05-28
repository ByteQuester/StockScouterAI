CREATE VIEW IF NOT EXISTS assets_liabilities_working_capital AS
SELECT *,
       ROUND(ASSETS_CURRENT - LIABILITIES_CURRENT, 2) AS Working_Capital
FROM raw_assets_liabilities;
