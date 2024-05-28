CREATE VIEW IF NOT EXISTS profitability_analysis AS
SELECT a.Entity,
       a.CIK,
       a.DATE,
       a.Year,
       a.Quarter,
       a.NET_INCOME_LOSS,
       a.REVENUES,
       a.OPS_INCOME_LOSS,
       a.PROFIT_MARGIN,
       b.Revenues_QoQ_Growth,
       b.OperatingIncome_QoQ_Growth,
       c.Expense_Ratio,
       a.REVENUES - a.OPS_INCOME_LOSS AS Operational_Expenses
FROM raw_profitability a
LEFT JOIN profitability_qoq_growth b ON a.CIK = b.CIK AND a.DATE = b.DATE
LEFT JOIN profitability_expense_ratio c ON a.CIK = c.CIK AND a.DATE = c.DATE;
