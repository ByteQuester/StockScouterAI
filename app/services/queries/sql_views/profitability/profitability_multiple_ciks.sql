-- Query for multiple CIKs
SELECT * FROM profitability_analysis WHERE CIK IN (?, ?, ?) AND DATE BETWEEN ? AND ?;
