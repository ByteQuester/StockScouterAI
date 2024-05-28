CREATE VIEW IF NOT EXISTS cash_flow_investing_trend AS
SELECT *,
       CASE WHEN CASH_FLOW_INVESTING > 0 THEN 'Investing Increase' ELSE 'Investing Decrease' END AS Investing_Trend
FROM raw_cash_flow;
