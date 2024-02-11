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
        MAX(CASE WHEN Metric = 'AssetsCurrent' THEN value ELSE NULL END) AS Assets,
        MAX(CASE WHEN Metric = 'Liabilities' THEN value ELSE NULL END) AS Liabilities,
        MAX(CASE WHEN Metric = 'StockholdersEquity' THEN value ELSE NULL END) AS StockholdersEquity
    FROM preprocessed_data
    GROUP BY EntityName, CIK, end_date, year, quarter
)

-- Step 3: Perform calculations
SELECT
    EntityName,
    CIK,
    end_date,
    Assets / 1000000 AS Assets_Million,
    Liabilities / 1000000 AS Liabilities_Million,
    StockholdersEquity / 1000000 AS StockholdersEquity_Million,
    CASE
        WHEN Assets IS NOT NULL AND Liabilities IS NOT NULL AND Liabilities != 0 THEN Assets / Liabilities
        ELSE NULL
    END AS AssetToLiabilityRatio,
    CASE
        WHEN Liabilities IS NOT NULL AND StockholdersEquity IS NOT NULL AND StockholdersEquity != 0 THEN Liabilities / StockholdersEquity
        ELSE NULL
    END AS DebtToEquityRatio,
    year,
    quarter
FROM pivoted_data;
