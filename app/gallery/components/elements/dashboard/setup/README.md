# Front-End Dashboard Configuration

## Overview

The front-end dashboard configuration is a crucial component of financial dashboard project. It is designed to provide interactive and dynamic visualizations of financial data through a tiered approach, catering to different levels of data analysis and user interaction needs. This document details the setup process for the second and third-tier dashboards, emphasizing the utilization of Streamlit alongside Plotly for server-side rendering and JSON for client-side visualization configurations.

## Dashboard Setup

The dashboard setup process involves configuring various widgets and charts to present financial data effectively. It spans across two main tiers:

### Second-Tier Dashboard

- **Purpose**: Focuses on delivering in-depth financial analysis directly within the server environment, making extensive use of Pandas for data manipulation and Plotly alongside Streamlit for visualization.

- **Base Configuration**:
  - **`SecondTierViewBase`**: Acts as the foundation for all second-tier dashboards, facilitating data loading, preprocessing, and basic UI setup.
  
### Third-Tier Dashboard

- **Purpose**: Aimed at enhancing client-side interactivity through dynamic visualizations configured via JSON, suitable for complex data representations and custom visualizations.

- **Abstract Setup**:
  - **`DashboardSetup` (ABC)**: An abstract base class that defines a standard for dashboard layouts and widget setups, enabling consistent and modular dashboard configurations.
  
### Extending Dashboard Configurations

#### Adding New Financial Analyses

1. **Subclass `SecondTierViewBase`**: For server-side visualizations, create a new subclass for each financial analysis domain, implementing specific data processing and visualization methods.
   
2. **Implement New `DashboardSetup` Subclass**: For client-side visualizations, define a new subclass that sets up widgets and content specific to the new analysis type.

#### Visualization Techniques

- Utilize `FinancialChart` for Plotly chart configurations in the second-tier dashboards.
- For the third-tier, extend the `DashboardSetup` with specific widget configurations and JSON transformations for client-side charts.

## Development Guide

### Implementing a New Dashboard View

1. **Define Analysis Class**: Start by creating a new analysis class that extends `SecondTierViewBase` or a new setup class extending `DashboardSetup` based on the tier.
   
2. **Data Processing and Metric Calculation**: Implement methods within the class to process data, calculate financial metrics, and generate insights.
   
3. **Visualization and Widget Configuration**: Utilize Plotly and Streamlit for the second tier or JSON configurations for the third tier to set up the visual components of the dashboard.
   
4. **Integration into Main Application**: Ensure the new dashboard component is accessible through the main application flow, with appropriate UI hooks and data loading mechanisms in place.

### Example Configuration

```python
class ProfitabilityDashboardDev(SecondTierViewBase):
    def __init__(self, cik):
        super().__init__(cik, query_type='Profitability')
        self.load_data()
        self.initialize_analysis()

    def calculate_metrics(self):
        # Implement profitability-specific metric calculations
        pass

    def render_charts(self):
        # Use FinancialChart for plotting
        pass
