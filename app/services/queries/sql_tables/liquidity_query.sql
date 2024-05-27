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
),

-- Step 3: Calculate quarter-over-quarter growth
qoq_growth AS (
    SELECT
        EntityName,
        CIK,
        end_date,
        CurrentAssets,
        CurrentLiabilities,
        LAG(CurrentAssets, 1) OVER (PARTITION BY EntityName ORDER BY end_date) AS Prev_CurrentAssets,
        LAG(CurrentLiabilities, 1) OVER (PARTITION BY EntityName ORDER BY end_date) AS Prev_CurrentLiabilities,
        year,
        quarter
    FROM pivoted_data
),

growth_data AS (
    SELECT
        *,
        CASE
            WHEN Prev_CurrentAssets IS NOT NULL AND Prev_CurrentAssets != 0 THEN
                (CurrentAssets - Prev_CurrentAssets) / Prev_CurrentAssets * 100
            ELSE NULL
        END AS CurrentAssets_QoQ_Growth,
        CASE
            WHEN Prev_CurrentLiabilities IS NOT NULL AND Prev_CurrentLiabilities != 0 THEN
                (CurrentLiabilities - Prev_CurrentLiabilities) / Prev_CurrentLiabilities * 100
            ELSE NULL
        END AS CurrentLiabilities_QoQ_Growth
    FROM qoq_growth
),

-- Step 4: Calculate the current ratio
final_output AS (
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
        CurrentAssets_QoQ_Growth,
        CurrentLiabilities_QoQ_Growth,
        year AS Year,
        quarter AS Quarter
    FROM growth_data
)

SELECT * FROM final_output;
