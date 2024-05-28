CREATE VIEW IF NOT EXISTS profitability_expense_ratio AS
SELECT *,
       ROUND ((REVENUES - OPS_INCOME_LOSS) / REVENUES * 100, 2) AS Expense_Ratio
FROM raw_profitability;
