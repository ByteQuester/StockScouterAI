CREATE VIEW IF NOT EXISTS cash_flow_analysis AS
SELECT a.ENTITY,
       a.CIK,
       a.DATE,
       a.Year,
       a.Quarter,
       a.CASH_FLOW_FINANCING,
       a.CASH_FLOW_INVESTING,
       a.CASH_FLOW_OPERATING,
       b.CASH_FLOW_FINANCING_YoY,
       b.CASH_FLOW_INVESTING_YoY,
       b.CASH_FLOW_OPERATING_YoY,
       c.Net_Cash_Flow,
       c.Positive_Cash_Flow,
       d.Operating_Efficiency_Ratio,
       e.Financing_Strategy,
       f.Investing_Trend
FROM raw_cash_flow a
LEFT JOIN cash_flow_yoy_growth b ON a.CIK = b.CIK AND a.DATE = b.DATE
LEFT JOIN cash_flow_summary_insights c ON a.CIK = c.CIK AND a.DATE = c.DATE
LEFT JOIN cash_flow_operating_efficiency d ON a.CIK = d.CIK AND a.DATE = d.DATE
LEFT JOIN cash_flow_financing_strategy e ON a.CIK = e.CIK AND a.DATE = e.DATE
LEFT JOIN cash_flow_investing_trend f ON a.CIK = f.CIK AND a.DATE = f.DATE;
