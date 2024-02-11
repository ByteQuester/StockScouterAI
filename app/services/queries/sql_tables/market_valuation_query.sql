SELECT 
    EntityName AS Entity,
    CIK,
    End AS Date,
    ROUND(SUM(CASE WHEN Metric = 'MarketCapitalization' THEN Value ELSE NULL END) / 1000000, 2) AS MarketCap,
    AVG(CASE WHEN Metric = 'EarningsPerShareBasic' THEN Value ELSE NULL END) AS EPS_Basic,
    AVG(CASE WHEN Metric = 'EarningsPerShareDiluted' THEN Value ELSE NULL END) AS EPS_Diluted,
    CASE
        WHEN AVG(CASE WHEN Metric = 'EarningsPerShareDiluted' THEN Value ELSE NULL END) > 0 THEN 
            ROUND(AVG(StockPrice) / NULLIF(AVG(CASE WHEN Metric = 'EarningsPerShareDiluted' THEN Value ELSE NULL END), 0), 2)
        ELSE NULL 
    END AS PE_Ratio,
    CASE 
        WHEN EXTRACT(MONTH FROM End) IN (1, 2, 3) THEN CONCAT('Q1-', EXTRACT(YEAR FROM End))
        WHEN EXTRACT(MONTH FROM End) IN (4, 5, 6) THEN CONCAT('Q2-', EXTRACT(YEAR FROM End))
        WHEN EXTRACT(MONTH FROM End) IN (7, 8, 9) THEN CONCAT('Q3-', EXTRACT(YEAR FROM End))
        ELSE CONCAT('Q4-', EXTRACT(YEAR FROM End))
    END AS Quarter
FROM 
    TEST_TABLE
-- Make sure to join with a table that has stock price data if it's not in the same table
LEFT JOIN 
    stock_price_table ON your_table_name.CIK = stock_price_table.CIK AND your_table_name.End = stock_price_table.Date
WHERE 
    Metric IN ('MarketCapitalization', 'EarningsPerShareBasic', 'EarningsPerShareDiluted')
GROUP BY 
    EntityName, CIK, End
ORDER BY 
    EntityName, CIK, End;
