
# Front-End Dashboard Configuration

## Overview

The front-end dashboard configuration is designed to provide interactive and dynamic visualizations of financial data through a tiered approach. It caters to different levels of data analysis and user interaction needs. This document details the setup process for the second and third-tier dashboards, emphasizing the utilization of Streamlit alongside Plotly for server-side rendering and JSON for client-side visualization configurations.

## Dashboard Setup

The dashboard setup process involves configuring various widgets and charts to present financial data effectively. It spans across three main tiers:

### General-Tier Dashboard

- **Purpose**: Provides a comprehensive overview of financial data, allowing users to visualize multiple metrics across different companies.
- **Key Metrics**: 
  - Assets vs Liabilities (ASSETS_CURRENT, LIABILITIES_CURRENT)
  - Debt to Equity Ratio (DEBT_TO_EQUITY_RATIO)
  - Cash Flow Summary (CASH_FLOW_OPERATING, CASH_FLOW_INVESTING, CASH_FLOW_FINANCING)
  - Profit Margin Trend (PROFIT_MARGIN)
  - Current Ratio Trend (CURRENT_RATIO)

- **Base Configuration**:
  - **`GeneralDashboardBase`**: Facilitates data loading, preprocessing, and basic UI setup.
  - **`FinancialChart`**: Unified chart rendering class that supports different chart types and configurations.

### Second-Tier Dashboard

- **Purpose**: Focuses on delivering in-depth financial analysis directly within the server environment, making extensive use of Pandas for data manipulation and Plotly alongside Streamlit for visualization.

- **Key Metrics**:
  - Assets & Liabilities
    - Assets vs Liabilities (ASSETS_CURRENT, LIABILITIES_CURRENT)
    - Debt to Equity Ratio (DEBT_TO_EQUITY_RATIO)
  - Cash Flow
    - Cash Flow Summary (CASH_FLOW_OPERATING, CASH_FLOW_INVESTING, CASH_FLOW_FINANCING)
  - Profitability
    - Profit Margin Trend (PROFIT_MARGIN)
  - Liquidity
    - Current Ratio Trend (CURRENT_RATIO)

- **Base Configuration**:
  - **`SecondTierViewBase`**: Acts as the foundation for all second-tier dashboards, facilitating data loading, preprocessing, and basic UI setup.

### Third-Tier Dashboard

- **Purpose**: Aimed at enhancing client-side interactivity through dynamic visualizations configured via JSON, suitable for complex data representations and custom visualizations.

- **Abstract Setup**:
  - **`DashboardSetup` (ABC)**: An abstract base class that defines a standard for dashboard layouts and widget setups, enabling consistent and modular dashboard configurations.

## Development Guide

### Implementing a New Dashboard View

1. **Define Analysis Class**: Create a new analysis class that extends `GeneralDashboardBase` or `SecondTierViewBase` based on the tier.
2. **Data Processing and Metric Calculation**: Implement methods within the class to process data, calculate financial metrics, and generate insights.
3. **Visualization and Widget Configuration**: Utilize the `FinancialChart` class for chart rendering. Configure the visual components of the dashboard using Plotly and Streamlit for server-side or JSON for client-side setups.
4. **Integration into Main Application**: Ensure the new dashboard component is accessible through the main application flow, with appropriate UI hooks and data loading mechanisms in place.

### Example Configuration

```python
# Example for Second-Tier Dashboard
class ProfitabilityDashboardDev(SecondTierViewBase):
    def __init__(self, ciks):
        super().__init__(ciks, query_type='Profitability')
        self.load_data()
        self.initialize_analysis()

    def calculate_metrics(self):
        # Implement profitability-specific metric calculations
        pass

    def render_charts(self):
        # Use FinancialChart for plotting
        pass
```

### Utilizing `FinancialChart` Class

The `FinancialChart` class supports various configurations to render different types of charts. (changed to `GeneralTierChart` and `SecondTierChart` for separation of concern)

```python
from general_tier import GeneralTierChart

def render_example_chart(data):
    GeneralTierChart(
        chart_type="bar",
        data=data,
        title="Example Chart",
        x_axis="DATE",
        y_axis=["METRIC1", "METRIC2"],
        bar_mode='group',
        color='ENTITY',
        bargap=0.15,
        bargroupgap=0.1
    ).render()
```

## Code Organization

The project is organized into different directories for each tier, with a unified `FinancialChart` class shared across both tiers for consistency.

### Project Structure

```plaintext
dashboard
├── __init__.py
├── layouts
│   ├── general
│   │   ├── __init__.py
│   │   ├── general_dashboard.py
│   │   ├── graph_renderers.py
│   │   └── main.py
│   ├── second_tier
│   │   ├── __init__.py
│   │   ├── assets_liabilities
│   │   │   ├── __init__.py
│   │   │   ├── assets_liabilities_dashboard.py
│   │   │   └── graph_renderers.py
│   │   ├── base.py
│   │   ├── cash_flow
│   │   │   ├── __init__.py
│   │   │   ├── cash_flow_dashboard.py
│   │   │   └── graph_renderers.py
│   │   ├── liquidity
│   │   │   ├── __init__.py
│   │   │   ├── liquidity_dashboard.py
│   │   │   └── graph_renderers.py
│   │   ├── main.py
│   │   └── profitability
│   │       ├── __init__.py
│   │       ├── profitability_dashboard.py
│   │       └── graph_renderers.py
│   └── third_tier
│       ├── __init__.py
│       ├── base.py
│       ├── main.py
├── setup
│   ├── __init__.py
│   ├── chart_register.py
│   ├── general_tier.py
│   ├── second_tier.py
│   └── third_tier.py
└── types
    ├── __init__.py
    └── types.py
```

This structure ensures a clear separation of concerns and modularity, making it easier to manage and extend the dashboard functionalities.

---

