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
        SUBSTRING(frame, 3, 4) AS year,   -- Extract year
        SUBSTRING(frame, 7, 2) AS quarter -- Extract quarter
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
        MAX(CASE WHEN Metric = 'NetIncomeLoss' THEN value ELSE NULL END) AS NetIncomeLoss,
        MAX(CASE WHEN Metric = 'Revenues' THEN value ELSE NULL END) AS Revenues,
        MAX(CASE WHEN Metric = 'OperatingIncomeLoss' THEN value ELSE NULL END) AS OperatingIncomeLoss
    FROM preprocessed_data
    GROUP BY EntityName, CIK, end_date, year, quarter
),

-- Step 3: Calculate previous quarter values for QoQ growth
previous_values AS (
    SELECT *,
           LAG(Revenues, 1) OVER (PARTITION BY EntityName ORDER BY end_date) AS Prev_Revenues,
           LAG(OperatingIncomeLoss, 1) OVER (PARTITION BY EntityName ORDER BY end_date) AS Prev_OperatingIncomeLoss
    FROM pivoted_data
),

-- Step 4: Perform Calculations
calculation_data AS (
    SELECT
        EntityName,
        CIK,
        end_date,
        year,
        quarter,
        Revenues,
        OperatingIncomeLoss,
        NetIncomeLoss,
        -- Calculate QoQ growth for revenues and operating income
        CASE WHEN Prev_Revenues IS NOT NULL AND Prev_Revenues != 0 THEN
            (Revenues - Prev_Revenues) / Prev_Revenues * 100
            ELSE NULL END AS Revenues_QoQ_Growth,
        CASE WHEN Prev_OperatingIncomeLoss IS NOT NULL AND Prev_OperatingIncomeLoss != 0 THEN
            (OperatingIncomeLoss - Prev_OperatingIncomeLoss) / Prev_OperatingIncomeLoss * 100
            ELSE NULL END AS OperatingIncome_QoQ_Growth,
        -- Calculate expense ratio
        CASE WHEN Revenues IS NOT NULL AND Revenues != 0 THEN
            ((Revenues - OperatingIncomeLoss) / Revenues) * 100
            ELSE NULL END AS Expense_Ratio,
        -- Calculate operational expenses
        Revenues - OperatingIncomeLoss AS Operational_Expenses
    FROM previous_values
),

-- Step 5: Aggregate data by quarter
summary_by_quarter AS (
    SELECT
        year,
        quarter,
        SUM(Revenues) AS Total_Revenues,
        AVG(Expense_Ratio) AS Average_Expense_Ratio
    FROM calculation_data
    GROUP BY year, quarter
)

-- Final output: select desired fields
SELECT
    ENTITY,
    CIK,
    DATE,
    year AS Year,
    quarter AS Quarter,
    NetIncomeLoss / 1000000 AS NetIncomeLoss_Million,
    Revenues / 1000000 AS Revenues_Million,
    OperatingIncomeLoss / 1000000 AS OperatingIncomeLoss_Million,
    Revenues_QoQ_Growth,
    OperatingIncome_QoQ_Growth,
    Expense_Ratio,
    Operational_Expenses / 1000000 AS Operational_Expenses_Million
FROM calculation_data;

-- Optionally select from summary_by_quarter to see aggregated data
-- SELECT * FROM summary_by_quarter;