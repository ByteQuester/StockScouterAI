TO BE UPDATED
# Front-End Modules 2/3

## Overview

The front-end modules of our financial dashboard project are designed to deliver dynamic, interactive visualizations and insights into financial data through two primary tiers: a server-side rendered dashboard and a client-side visualization layer utilizing JSON for chart configurations. This document outlines the structure and development process for integrating financial analyses into these visualization tiers.

## Second-Tier Dashboard

The second-tier dashboard is focused on providing in-depth financial analysis and insights directly within the server environment, leveraging the powerful data manipulation and visualization capabilities of Pandas, Plotly, and Streamlit.

### Base Components

- **`SecondTierViewBase`**: Serves as the foundational class for all second-tier dashboards, handling data loading, preprocessing, and the basic UI setup using Streamlit.

### Development Process

1. **Data Analysis Integration**:
   - Subclasses of `SecondTierViewBase` are created for specific financial analysis domains (e.g., Profitability, Cash Flow).
   - These subclasses implement methods for data processing, metric calculation, and insight generation based on the preprocessed data.

2. **Visualization**:
   - Utilize Plotly Express through the `FinancialChart` class to create interactive charts based on the calculated metrics.
   - Streamlit widgets and layout options are used to present data insights and visualizations interactively.

### Extending the Dashboard

To introduce a new financial analysis domain or visualization:
1. **Create a New Subclass**: Derive from `SecondTierViewBase`, implementing necessary data processing and insight generation methods.
2. **Implement Visualization Methods**: Use `FinancialChart` and Streamlit APIs to design and render new visualizations.
3. **Update UI**: Integrate the new dashboard component into the main application flow, ensuring it's accessible from the UI.

## Visualization with JSON Charts

For client-side visualizations that require flexibility and dynamic data representation, transforming data into JSON format enables the use of various JavaScript charting libraries.

### Transformation Process

- **`JSONDataTransformer`**: Handles the conversion of Pandas DataFrames into JSON structures suitable for visualization purposes.
- Data is processed through specific transformer subclasses (`AssetsLiabilitiesTransformer`, `CashFlowTransformer`, etc.) that encapsulate the logic for converting financial metrics into a JSON format.

### Development Guide

1. **Define New Transformer**: For new types of financial data visualization, create a subclass of `BaseTransformer` that implements the transformation logic into the desired JSON structure.
2. **Integration**: Utilize the `JSONDataTransformer` to apply the new transformer to the relevant dataset, generating the JSON output.
3. **Front-End Implementation**: Use the generated JSON to feed data into client-side charting solutions, creating dynamic and interactive visualizations.

## Conclusion

The modular design of the front-end modules allows for scalable and flexible development of financial dashboards, separating concerns between data analysis, transformation, and visualization.
