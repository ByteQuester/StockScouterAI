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
)

-- Step 3: Perform calculations
SELECT
    EntityName AS ENTITY,
    CIK,
    end_date AS DATE,
    NetIncomeLoss / 1000000 AS NetIncomeLoss_Million,
    Revenues / 1000000 AS Revenues_Million,
    OperatingIncomeLoss / 1000000 AS OperatingIncomeLoss_Million,
    CASE
        WHEN NetIncomeLoss IS NOT NULL AND Revenues IS NOT NULL AND Revenues != 0 THEN (NetIncomeLoss / Revenues) * 100
        ELSE NULL
    END AS ProfitMarginPercent,
    year AS Year,
    quarter AS Quarter
FROM pivoted_data;
