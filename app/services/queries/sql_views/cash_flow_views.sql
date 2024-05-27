-- Create a view for calculating year-over-year growth
CREATE VIEW IF NOT EXISTS cash_flow_yoy_growth AS
WITH preprocessed_data AS (
    SELECT *,
           LAG(CASH_FLOW_FINANCING, 4) OVER (PARTITION BY ENTITY ORDER BY DATE) AS Prev_CASH_FLOW_FINANCING,
           LAG(CASH_FLOW_INVESTING, 4) OVER (PARTITION BY ENTITY ORDER BY DATE) AS Prev_CASH_FLOW_INVESTING,
           LAG(CASH_FLOW_OPERATING, 4) OVER (PARTITION BY ENTITY ORDER BY DATE) AS Prev_CASH_FLOW_OPERATING
    FROM raw_cash_flow
)
SELECT
    ENTITY,
    CIK,
    DATE,
    Year,
    Quarter,
    CASH_FLOW_FINANCING,
    CASH_FLOW_INVESTING,
    CASH_FLOW_OPERATING,
    CASE WHEN Prev_CASH_FLOW_FINANCING IS NOT NULL THEN
        ROUND((CASH_FLOW_FINANCING - Prev_CASH_FLOW_FINANCING) / Prev_CASH_FLOW_FINANCING * 100, 2)
        ELSE NULL END AS CASH_FLOW_FINANCING_YoY,
    CASE WHEN Prev_CASH_FLOW_INVESTING IS NOT NULL THEN
        ROUND((CASH_FLOW_INVESTING - Prev_CASH_FLOW_INVESTING) / Prev_CASH_FLOW_INVESTING * 100, 2)
        ELSE NULL END AS CASH_FLOW_INVESTING_YoY,
    CASE WHEN Prev_CASH_FLOW_OPERATING IS NOT NULL THEN
        ROUND((CASH_FLOW_OPERATING - Prev_CASH_FLOW_OPERATING) / Prev_CASH_FLOW_OPERATING * 100, 2)
        ELSE NULL END AS CASH_FLOW_OPERATING_YoY
FROM preprocessed_data;

-- Create a view for calculating summary insights
CREATE VIEW IF NOT EXISTS cash_flow_summary_insights AS
SELECT *,
       (CASH_FLOW_FINANCING + CASH_FLOW_INVESTING + CASH_FLOW_OPERATING) AS Net_Cash_Flow,
       CASE WHEN (CASH_FLOW_FINANCING + CASH_FLOW_INVESTING + CASH_FLOW_OPERATING) > 0 THEN 1 ELSE 0 END AS Positive_Cash_Flow
FROM raw_cash_flow;

-- Create a view for calculating operating efficiency
CREATE VIEW IF NOT EXISTS cash_flow_operating_efficiency AS
SELECT *,
       CASH_FLOW_OPERATING / MAX(CASH_FLOW_OPERATING) OVER (PARTITION BY ENTITY) AS Operating_Efficiency_Ratio
FROM raw_cash_flow;

-- Create a view for calculating financing strategy
CREATE VIEW IF NOT EXISTS cash_flow_financing_strategy AS
SELECT *,
       CASE WHEN CASH_FLOW_FINANCING < 0 THEN 'Debt Reduction' ELSE 'Debt Acquisition' END AS Financing_Strategy
FROM raw_cash_flow;

-- Create a view for calculating investing trend
CREATE VIEW IF NOT EXISTS cash_flow_investing_trend AS
SELECT *,
       CASE WHEN CASH_FLOW_INVESTING > 0 THEN 'Investing Increase' ELSE 'Investing Decrease' END AS Investing_Trend
FROM raw_cash_flow;

-- Combine all calculations into a single view
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
