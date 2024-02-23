# Financial Data (Pre)Processing 

## Table of Contents

- [Overview](#overview)
- [Module Components](#module-components)
- [Usage Examples](#usage-examples)
- [Scalability and Extension](#scalability-and-extension)
- [Contributing](#contributing)
- [License](#license)

## Overview

This module is central to processing financial data from SEC filings, aimed at supporting scalable financial analysis. It includes classes designed for the structured filtering, cleaning, sorting, and preparation of annual and quarterly financial datasets.

| Component              | Description                                                     | Scalability Step   |
|------------------------|-----------------------------------------------------------------|--------------------|
| FinancialDataProcessor | Abstract base class for setting up the data processing framework | Base for extension |
| AnnualDataProcessor    | Subclass for processing annual financial data                   | Annual data analysis |
| QuarterlyDataProcessor | Subclass for processing quarterly financial data                | Quarterly data analysis |

#### FinancialDataProcessor

- **Purpose:** Establishes a structured approach for data processing tasks.
- **Key Features:**
  - Abstract methods for data processing.
  - Utility methods for common data manipulation tasks.

#### AnnualDataProcessor & QuarterlyDataProcessor

- **Purpose:** Implement specific data processing logic for annual and quarterly data.
- **Key Features:**
  - Inherits from FinancialDataProcessor.
  - Tailored methods for filtering, cleaning, and sorting data.

## Usage Examples

```python
# Annual Data Processing
annual_data = AnnualDataProcessor(dataframe)
processed_annual = annual_data.process_data(['Revenue', 'Expenses'])

# Quarterly Data Processing
quarterly_data = QuarterlyDataProcessor(dataframe)
processed_quarterly = quarterly_data.process_data(['NetIncome', 'TotalAssets'])
