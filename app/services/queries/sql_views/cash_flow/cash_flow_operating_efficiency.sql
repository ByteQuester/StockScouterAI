CREATE VIEW IF NOT EXISTS cash_flow_operating_efficiency AS
SELECT *,
       CASH_FLOW_OPERATING / MAX(CASH_FLOW_OPERATING) OVER (PARTITION BY ENTITY) AS Operating_Efficiency_Ratio
FROM raw_cash_flow;
