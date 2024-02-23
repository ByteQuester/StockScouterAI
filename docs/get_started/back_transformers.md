# Data Transformation 

## Overview

This module is dedicated to transforming processed financial data into JSON format, optimized for chart visualizations and dashboard presentations of **Third Tier View**. 

## Scalability Framework

The transformation process is designed with scalability in mind, allowing for easy integration of new data tables and transformation techniques.

### Core Components

- `JSONDataTransformer`: Central to converting processed data into JSON, preparing it for visualization.
- `BaseTransformer` and Subclasses: Implement specific transformation techniques for different financial metrics and chart types.

### Adding New Data Tables

To introduce new data tables for transformation:
1. **Define a New Transformer**: Create a subclass of `BaseTransformer`, implementing the `transform_all` method with logic specific to the new data table.
2. **Integrate with `JSONDataTransformer`**: Update `JSONDataTransformer` to handle the new transformer subclass, ensuring the processed data is transformed and stored as JSON.

### Transformation Techniques

| Component                | Description                                                                                       | Implementation Guide                                                                 |
|--------------------------|---------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| `BaseTransformer`        | Abstract base offering foundational transformation methods.                                       | Subclass and override `transform_all` with specific logic for new financial metrics. |
| `AssetsLiabilitiesTransformer` | Transforms Assets & Liabilities data for visualization.                                          | Demonstrates line, bar, and datagrid transformations.                                |
| `CashFlowTransformer`    | Dedicated to transforming Cash Flow metrics into a visually representable format.                 | Focuses on cash flow visualizations, adaptable to new metrics.                       |
| `LiquidityTransformer`   | Converts Liquidity data for chart visualization, emphasizing current assets and liabilities.     | Example of ratio-based visual data transformation.                                   |
| `ProfitabilityTransformer` | Transforms Profitability metrics, suitable for analyzing margins and growth.                     | Illustrates complex chart transformations, including line and divergence charts.     |

## Extending the Module

Enhancing the data transformation capabilities involves:
- **Identifying New Metrics**: Determine new financial metrics requiring visualization.
- **Developing Transformer Logic**: Implement transformation logic in a new `BaseTransformer` subclass.
- **Integrating Transformer**: Update the transformation process to include the new subclass, ensuring its output is correctly formatted for the intended visualization.

## Technical Implementation

To add a new transformation technique:
1. Create a subclass of `BaseTransformer`.
2. Implement the `transform_all` method, detailing how the data should be transformed into JSON format for the new metric.
3. Update `JSONDataTransformer` to recognize and apply the new subclass based on the data category or specific transformation requirements.

