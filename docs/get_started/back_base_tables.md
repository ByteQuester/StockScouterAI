# Base Production Line

## Overview

First step of queries in subsequent stages of the project to populate a base dataframe for all (general, second and third tier)
views (_aka Base Production Line_).

## Module Structure and Scalability Steps

The module is structured around a base class for generic financial data queries and specialized subclasses for targeted financial analyses. Below is an overview of each component and its place in the project's scalability framework.

### Base Class

| Component | Responsibility | Scalability Step |
|-----------|----------------|------------------|
| `FinancialQueryBase` | Provides foundational methods for data validation, transformation, and preparation. Establishes a pattern for extending financial queries. | **Base for Scalability**|

### Subclasses and Their Roles

Each subclass extends `FinancialQueryBase` to perform specific financial calculations, playing a pivotal role in populating the base dataset with financial metrics.

| Query Class | Description | Key Responsibilities | Scalability Step |
|-------------|-------------|----------------------|------------------|
| `ProfitabilityQuery` | Calculates profitability metrics. | Adds calculations like Profit Margin Percent. Prepares data for both direct analysis and visualization layers. | **Metric Expansion**: Demonstrates the model for introducing new metrics into the analysis. |
| `CashFlowQuery` | Analyzes cash flow activities. | Focuses on operating, investing, and financing activities cash flows. | **Analysis Depth**: Enhances the dataset by providing detailed cash flow insights. |
| `LiquidityQuery` | Assesses liquidity status. | Calculates ratios such as Current Ratio to evaluate liquidity. | **Financial Health Analysis**: Offers insights into the company's short-term financial health. |
| `AssetsLiabilityQuery` | Examines assets and liabilities. | Computes ratios like Asset to Liability and Debt to Equity. | **Balance Sheet Analysis**: Expands the dataset with key balance sheet ratios for deeper financial scrutiny. |

| Query Class            | Key Metrics Example                                                                                                                      |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `ProfitabilityQuery`   | 'NetIncomeLoss', 'OperatingIncomeLoss', 'Revenues'                                                                                       |
| `CashFlowQuery`        | 'NetCashProvidedByUsedInOperatingActivities', 'NetCashProvidedByUsedInInvestingActivities', 'NetCashProvidedByUsedInFinancingActivities' |
| `LiquidityQuery`       | 'AssetsCurrent', 'LiabilitiesCurrent'                                                                                                    |
| `AssetsLiabilityQuery` | 'AssetsCurrent', 'LiabilitiesCurrent', 'StockholdersEquity'                                                                              |

## Extending the Module

This module is designed for scalability, allowing for the introduction of new financial analyses with minimal friction. To add a new query class:

1. **Create a New Subclass**: Derive from `FinancialQueryBase`, implementing specific financial calculations.
2. **Implement `add_calculations` Method**: Define the calculations unique to your financial analysis.
3. **Use `run_query` for Data Preparation**: Leverage inherited methods for data validation, pivoting, and scaling.

