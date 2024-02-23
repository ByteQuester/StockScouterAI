# Front-End Modules 3/3

## Overview

The third-tier dashboard is an advanced component of our financial dashboard project, designed to enable client-side interactive visualizations. This tier leverages a modular approach to dynamically render financial data into customizable widgets and charts, utilizing a client-side framework for enhanced interactivity and user experience. This document details the configuration process for the third-tier dashboards, focusing on the use of Streamlit for dashboard layout and custom widgets for visualization.
## Third-Tier Dashboard

The third-tier dashboard architecture is built around a series of base and subclass setups that dictate the layout, data processing, and visualization components of each dashboard.
### Base Components

- **`DashboardBase`**: An abstract base class that outlines the standard lifecycle and structure for dynamic dashboards. It includes methods for initializing the sidebar, loading and filtering data, setting up widgets, and rendering the dashboard content.

### Dashboard Setup Process

1. **Widget Configuration**:
   - Dashboard widgets are set up through subclasses that extend `DashboardBase`, specifying widgets like editors, line charts, cards, etc., tailored to the financial analysis domain (e.g., Profitability, Cash Flow).

2. **Data Processing and Visualization**:
   - Each subclass implements its own data processing methods, transforming raw financial data into insightful visualizations and interactive elements.

### Extending the Third-Tier Dashboards

To introduce a new financial analysis domain or enhance existing dashboards:

1. **Define a New Subclass**: Create a subclass of `DashboardBase` for the new dashboard, implementing abstract methods for data setup, widget configuration, and content rendering.

2. **Implement Data Processing and Widget Setup**:
   - Utilize provided UI components and Streamlit widgets to design and implement the visualization logic specific to the new financial analysis domain.

3. **Content Rendering**:
   - Override the `render_dashboard` method to dictate how the dashboard and its widgets are displayed to the user.

### Example: Profitability Dashboard

```python
class ProfitabilityDashboard(DashboardBase):
    def __init__(self, cik: str):
        super().__init__(cik, "Profitability")

    def setup_widgets(self):
        # Configuration for Profitability-specific widgets
        pass

    def setup_content(self):
        # Process data and setup dashboard content specific to Profitability
        pass

    def render_specific_widgets(self):
        # Render widgets specific to the Profitability dashboard
        pass
