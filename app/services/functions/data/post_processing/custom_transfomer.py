from typing import Dict, List, Union

import pandas as pd

from app.services.functions.transformers.transformers_base import \
    BaseTransformer
from app.services.types import (ASSETS_LIABILITIES_BAR_METRICS,
                                ASSETS_LIABILITIES_LINE_METRICS,
                                CASH_FLOW_CHARTS_METRICS,
                                LIQUIDITY_BAR_METRICS, LIQUIDITY_LINE_METRICS,
                                PROFITABILITY_LINE_METRICS,
                                PROFITABILITY_MARGIN_LINE_METRIC)


class CustomTransformer(BaseTransformer):
    """
    A custom transformer for transforming data for different types of charts.

    This class extends the BaseTransformer and utilizes its methods to
    transform data for line charts, bar charts, and data grids.

    Attributes:
        metrics: A list of metric names to transform.
    """

    def __init__(self, df: pd.DataFrame, metrics: List[str]) -> None:
        """
        Initializes the CustomTransformer with a DataFrame and metrics.

        Args:
            df: A pandas DataFrame containing the data to transform.
            metrics: A list of metric names to transform.

        Raises:
            ValueError: If the df is not a pandas DataFrame or metrics is not a list.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df must be a pandas DataFrame")
        super().__init__(df)
        if not isinstance(metrics, list):
            raise ValueError("metrics must be a list of strings")
        self.metrics = metrics

    def transform_all(
        self
    ) -> Dict[str, Union[List[Dict[str, Union[str, float]]], List[Dict[
            str, Union[str, float, None]]]]]:
        """
        Transforms data using the provided metrics for different chart types.

        Returns:
            Dict[str, Union[List[Dict[str, Union[str, float]]], List[Dict[str, Union[str, float, None]]]]]:
                Transformed data for line charts, bar charts, and datagrid.
        """
        return {
            "line_chart": self.transform_for_line_chart(self.metrics),
            "bar_chart": self.transform_for_bar_chart(self.metrics),
            "data_grid": self.transform_data_for_datagrid(),
        }
