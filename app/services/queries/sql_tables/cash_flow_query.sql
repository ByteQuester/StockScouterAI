-- Step 1: Preprocessing
WITH preprocessed_data AS (
    SELECT
        EntityName,
        CIK,
        Metric,
        CAST(end AS DATE) AS end_date,
        value,
        accn,
        fy,
        fp,
        form,
        filed,
        frame,
        SUBSTRING(frame, 3, 4) AS year,
        SUBSTRING(frame, 7, 2) AS quarter
    FROM test_table
    WHERE frame IS NOT NULL AND frame LIKE 'CY____Q_%'
),

-- Step 2: Pivot the table
pivoted_data AS (
    SELECT
        EntityName,
        CIK,
        end_date,
        year,
        quarter,
        MAX(CASE WHEN Metric = 'CashFlowFinancing' THEN value ELSE NULL END) AS CashFlowFinancing,
        MAX(CASE WHEN Metric = 'CashFlowInvesting' THEN value ELSE NULL END) AS CashFlowInvesting,
        MAX(CASE WHEN Metric = 'CashFlowOperating' THEN value ELSE NULL END) AS CashFlowOperating
    FROM preprocessed_data
    GROUP BY EntityName, CIK, end_date, year, quarter
),

-- Step 3: Calculate year-over-year growth
yoy_data AS (
    SELECT
        *,
        LAG(CashFlowFinancing, 1) OVER (PARTITION BY EntityName ORDER BY end_date) AS Prev_CashFlowFinancing,
        LAG(CashFlowInvesting, 1) OVER (PARTITION BY EntityName ORDER BY end_date) AS Prev_CashFlowInvesting,
        LAG(CashFlowOperating, 1) OVER (PARTITION BY EntityName ORDER BY end_date) AS Prev_CashFlowOperating
    FROM pivoted_data
),

growth_data AS (
    SELECT
        *,
        ((CashFlowFinancing - Prev_CashFlowFinancing) / Prev_CashFlowFinancing) * 100 AS CashFlowFinancing_YoY,
        ((CashFlowInvesting - Prev_CashFlowInvesting) / Prev_CashFlowInvesting) * 100 AS CashFlowInvesting_YoY,
        ((CashFlowOperating - Prev_CashFlowOperating) / Prev_CashFlowOperating) * 100 AS CashFlowOperating_YoY
    FROM yoy_data
),

-- Step 4: Summary insights and efficiency ratios
summary_efficiency AS (
    SELECT
        *,
        CashFlowFinancing + CashFlowInvesting + CashFlowOperating AS Net_Cash_Flow,
        CASE WHEN (CashFlowFinancing + CashFlowInvesting + CashFlowOperating) > 0 THEN 'True' ELSE 'False' END AS Positive_Cash_Flow,
        CashFlowOperating / MAX(CashFlowOperating) OVER (PARTITION BY EntityName) AS Operating_Efficiency_Ratio,
        CASE 
            WHEN CashFlowFinancing < 0 THEN 'Debt Reduction' 
            ELSE 'Debt Acquisition' 
        END AS Financing_Strategy,
        CASE 
            WHEN CashFlowInvesting > 0 THEN 'Investing Increase' 
            ELSE 'Investing Decrease' 
        END AS Investing_Trend
    FROM growth_data
)

-- Final selection
SELECT
    EntityName,
    CIK,
    end_date,
    year,
    quarter,
    Net_Cash_Flow,
    Positive_Cash_Flow,
    Operating_Efficiency_Ratio,
    Financing_Strategy,
    Investing_Trend,
    CashFlowFinancing_YoY,
    CashFlowInvesting_YoY,
    CashFlowOperating_YoY
FROM summary_efficiency;