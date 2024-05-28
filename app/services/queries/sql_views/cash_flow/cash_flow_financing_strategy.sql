CREATE VIEW IF NOT EXISTS cash_flow_financing_strategy AS
SELECT *,
       CASE WHEN CASH_FLOW_FINANCING < 0 THEN 'Debt Reduction' ELSE 'Debt Acquisition' END AS Financing_Strategy
FROM raw_cash_flow;
