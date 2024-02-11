SELECT 
    EntityName AS Entity,
    CIK,
    End AS Date,
    ROUND(SUM(CASE WHEN Metric = 'NetCashProvidedByUsedInOperatingActivities' THEN Value ELSE NULL END) / 1000000, 2) AS CashFlow_Operating,
    ROUND(SUM(CASE WHEN Metric = 'NetCashProvidedByUsedInInvestingActivities' THEN Value ELSE NULL END) / 1000000, 2) AS CashFlow_Investing,
    ROUND(SUM(CASE WHEN Metric = 'NetCashProvidedByUsedInFinancingActivities' THEN Value ELSE NULL END) / 1000000, 2) AS CashFlow_Financing,
    CASE
        WHEN EXTRACT(MONTH FROM End) IN (1, 2, 3) THEN CONCAT('Q1-', EXTRACT(YEAR FROM End))
        WHEN EXTRACT(MONTH FROM End) IN (4, 5, 6) THEN CONCAT('Q2-', EXTRACT(YEAR FROM End))
        WHEN EXTRACT(MONTH FROM End) IN (7, 8, 9) THEN CONCAT('Q3-', EXTRACT(YEAR FROM End))
        ELSE CONCAT('Q4-', EXTRACT(YEAR FROM End))
    END AS Quarter
FROM 
    test_table
WHERE 
    Metric IN ('NetCashProvidedByUsedInOperatingActivities', 'NetCashProvidedByUsedInInvestingActivities', 'NetCashProvidedByUsedInFinancingActivities')
GROUP BY 
    EntityName, CIK, End
ORDER BY 
    EntityName, CIK, End;
