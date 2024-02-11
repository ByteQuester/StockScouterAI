-- Step 1: Preprocessing
WITH preprocessed_data AS (
    SELECT
        EntityName,
        CIK,
        Metric,
        CAST(end AS DATE) AS end_date,
        value,
        SUBSTRING(frame, 3, 4) AS year,   -- Extract year
        SUBSTRING(frame, 7, 2) AS quarter -- Extract quarter
    FROM test_table
    WHERE frame IS NOT NULL AND frame LIKE 'CY____Q_%'
      AND Metric IN ('AssetsCurrent', 'LiabilitiesCurrent')
),

-- Step 2: Pivot the table
pivoted_data AS (
    SELECT
        EntityName,
        CIK,
        end_date,
        year,
        quarter,
        MAX(CASE WHEN Metric = 'AssetsCurrent' THEN value ELSE NULL END) AS CurrentAssets,
        MAX(CASE WHEN Metric = 'LiabilitiesCurrent' THEN value ELSE NULL END) AS CurrentLiabilities
    FROM preprocessed_data
    GROUP BY EntityName, CIK, end_date, year, quarter
)

-- Step 3: Perform calculations
SELECT
    EntityName AS ENTITY,
    CIK,
    end_date AS DATE,
    CurrentAssets / 1000000 AS CurrentAssets_Million,
    CurrentLiabilities / 1000000 AS CurrentLiabilities_Million,
    CASE
        WHEN CurrentLiabilities > 0 THEN CurrentAssets / CurrentLiabilities
        ELSE NULL
    END AS CurrentRatio,
    year AS Year,
    quarter AS Quarter
FROM pivoted_data;
