# Development Tiers

## Overview

The Development Tier represents as a middle stage in the data analysis pipeline: entering the **Second Tier View**, focusing on dynamic and exploratory data analysis and laying the groundwork for potential inclusion in the base query set for wider application in **Third Tier View**.

## Purpose

This tier allows for the exploration of new metrics, ratios, and financial analyses that can provide deeper insights into financial health, operational efficiency, profitability, and liquidity. It serves as a testing ground for developing and refining analytical methods before their formal integration into the production pipeline.

## Key Components

| Class                         | Description                                                                                                     | Example Metrics                        |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------|----------------------------------------|
| `AssetsLiabilitiesEquityAnalysis` | Calculates growth and assesses the financial structure through various asset, liability, and equity metrics.   | QoQ Growth, Working Capital            |
| `CashFlowAnalysis`             | Focuses on analyzing cash flow movements and providing insights into operational, investing, and financing activities. | YoY Growth, Cash Flow Efficiency       |
| `LiquidityAnalysis`            | Examines liquidity ratios and metrics to gauge short-term financial health.                                      | Quick Ratio, Current Ratio             |
| `ProfitabilityFinancialAnalysis` | Evaluates profitability and operational efficiency through various profitability ratios and metrics.            | Expense Ratio, Earnings Volatility     |

## Scalability and Integration

### Integration into Base Queries

Successful and valuable analyses developed within this tier may be integrated into the base query set (`add_calculations` method within `query_base.py` of [~/app/services/queries/base_tables]() (**Third Tier View**) or specific subclasses..

### Adding New Analyses

1. **Identify New Metrics:** Determine metrics or analyses that could provide additional insights.
2. **Implement Analysis Logic:** Develop the logic for calculating these metrics within a new or existing class in this tier.
3. **Evaluate and Refine:** Test the new analyses on relevant datasets, refine calculations, and assess their potential value for broader application.
4. **Integration Proposal:** Propose the integration of successful analyses into the base production line for inclusion in processed datasets.

## Example Usage

```python
from app.services.service_manager import DataPipelineIntegration
from app.gallery.util import DataLoader

# Define cik and query type
cik='0000012927'
query = 'Profitability'

# Load your dataset
data_pipeline = DataPipelineIntegration(cik_number=cik, use_snowflake=False)
df = data_pipeline.fetch_data()
data_pipeline.preprocess_data(df)
df = DataLoader().load_csv_data(cik_number=cik ,query_type=query)

# Initialize the analysis class
profitability_analysis = ProfitabilityFinancialAnalysis(df)

# Perform specific calculations
profitability_analysis.calculate_qoq_growth('REVENUES')
profitability_analysis.calculate_expense_ratio()

# Review the modified DataFrame
print(profitability_analysis.df.head())
