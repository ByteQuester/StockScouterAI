from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Union

import pandas as pd

from app.services.types import (ASSETS_LIABILITIES_BAR_METRICS,
                                ASSETS_LIABILITIES_LINE_METRICS,
                                CASH_FLOW_CHARTS_METRICS,
                                LIQUIDITY_BAR_METRICS, LIQUIDITY_LINE_METRICS,
                                PROFITABILITY_LINE_METRICS,
                                PROFITABILITY_MARGIN_LINE_METRIC)

from .interpolation import InterpolationTransformer


class BaseTransformer(ABC):

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialize the base transformer with a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be transformed.
        """
        self.df = df

    def transform_for_bar_chart(
            self, metrics: List[str]) -> List[Dict[str, Union[str, float]]]:
        """
        Transform the data for a bar chart.

        Args:
            metrics (List[str]): List of metric names to transform.

        Returns:
            List[Dict[str, Union[str, float]]]: Transformed data suitable for a bar chart.
        """
        transformed_data = {}
        for _, row in self.df.iterrows():
            date_formatted = self.format_date(row)
            if date_formatted not in transformed_data:
                transformed_data[date_formatted] = {"Date": date_formatted}

            for metric in metrics:
                metric_key = metric + "Value"
                color_key = metric + "Color"
                transformed_data[date_formatted][metric_key] = float(
                    row[metric]) if pd.notna(row[metric]) else None
                transformed_data[date_formatted][
                    color_key] = f"hsl({hash(metric) % 360}, 70%, 50%)"

        return list(transformed_data.values())

    def transform_for_complex_chart(
            self, metrics: List[str]) -> List[Dict[str, Union[str, float]]]:
        """
        Transform the data for a complex chart with positive and negative series.

        Args:
            metrics (List[str]): List of metric names to transform.

        Returns:
            List[Dict[str, Union[str, float]]]: Transformed data suitable for a complex chart.
        """
        transform = InterpolationTransformer(self.df)

        # If metrics is a list with one item, extract that item to pass as a string
        metric_to_pass = metrics[0] if len(metrics) == 1 else metrics
        # Ensure metric_to_pass is treated correctly within InterpolationTransformer

        transformed_data = transform.stream(metric_to_pass)
        return transformed_data

    def transform_for_line_chart(
            self, metrics: List[str]) -> List[Dict[str, Union[str, float]]]:
        """
        Transform the data for a line chart.

        Args:
            metrics (List[str]): List of metric names to transform.

        Returns:
            List[Dict[str, Union[str, float]]]: Transformed data suitable for a line chart.
        """
        transformed_data = []
        for metric in metrics:
            line_data = {
                "id": metric,
                "color": f"hsl({hash(metric) % 360}, 70%, 50%)",
                "data": []
            }
            for _, row in self.df.iterrows():
                date_formatted = self.format_date(row)
                y_value = float(row[metric]) if pd.notna(row[metric]) else None
                line_data["data"].append({"x": date_formatted, "y": y_value})
            transformed_data.append(line_data)
        return transformed_data

    def transform_data_for_datagrid(
            self) -> List[Dict[str, Union[int, str, float, None]]]:
        """
        Transform the data for a datagrid.

        Returns:
            List[Dict[str, Union[int, str, float, None]]]: Transformed data suitable for a datagrid.
        """
        # Common columns that are consistent across datasets
        common_columns = ['ENTITY', 'CIK', 'DATE', 'Year', 'Quarter']
        middle_columns = [
            col for col in self.df.columns if col not in common_columns
        ]

        transformed_data = []
        for idx, row in self.df.iterrows():
            transformed_row = {"id": idx + 1, "year": self.format_date(row)}

            # Process each of the middle columns and use their actual names
            for col in middle_columns:
                value = row[col]
                try:
                    transformed_row[col] = float(value) if pd.notna(
                        value) else None
                except ValueError:
                    transformed_row[col] = value

            transformed_data.append(transformed_row)

        return transformed_data

    def format_date(self, row: pd.Series) -> str:
        """
        Format the date from the DataFrame row.

        Args:
            row (pd.Series): A row from the DataFrame containing the data.

        Returns:
            str: The formatted date string.
        """
        date_str = row["DATE"]
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m")

    @abstractmethod
    def transform_all(self) -> Union[Dict, pd.DataFrame]:
        """
        Transform the data based on the specific transformer's logic.

        Returns:
            Union[Dict, pd.DataFrame]: Transformed data in a format suitable for the specific chart types.
        """
        pass


class AssetsLiabilitiesTransformer(BaseTransformer):

    def transform_all(self):
        """
        Transform data for Assets & Liabilities category.

        Returns:
            Dict[str, List[Dict[str, Union[str, float]]]]: Transformed data for line, bar and datagrid charts
        """
        return {
            "line_chart":
            self.transform_for_line_chart(
                ASSETS_LIABILITIES_LINE_METRICS.value),
            "bar_chart":
            self.transform_for_bar_chart(ASSETS_LIABILITIES_BAR_METRICS.value),
            "data_grid":
            self.transform_data_for_datagrid(),
        }


class CashFlowTransformer(BaseTransformer):

    def transform_all(self) -> Dict[str, List[Dict[str, Union[str, float]]]]:
        """
        Transform data for Cash Flow category.

        Returns:
            Dict[str, List[Dict[str, Union[str, float]]]]: Transformed data for line, bar and datagrid charts.
        """
        return {
            "line_chart":
            self.transform_for_line_chart(CASH_FLOW_CHARTS_METRICS.value),
            "bar_chart":
            self.transform_for_bar_chart(CASH_FLOW_CHARTS_METRICS.value),
            "data_grid":
            self.transform_data_for_datagrid(),
        }


class LiquidityTransformer(BaseTransformer):

    def transform_all(self) -> Dict[str, List[Dict[str, Union[str, float]]]]:
        """
        Transform data for Liquidity category.

        Returns:
            Dict[str, List[Dict[str, Union[str, float]]]]: Transformed data for line, bar and datagrid charts.
        """
        return {
            "line_chart":
            self.transform_for_line_chart(LIQUIDITY_LINE_METRICS.value),
            "bar_chart":
            self.transform_for_bar_chart(LIQUIDITY_BAR_METRICS.value),
            "data_grid":
            self.transform_data_for_datagrid(),
        }


class ProfitabilityTransformer(BaseTransformer):

    def transform_all(
        self
    ) -> Dict[str, Union[List[Dict[str, Union[str, float]]], List[Dict[
            str, Union[str, float, None]]]]]:
        """
        Transform data for Profitability category.

        Returns:
            Dict[str, Union[List[Dict[str, Union[str, float]]], List[Dict[str, Union[str, float, None]]]]]:
                Transformed data for line charts, complex charts, bar charts, datagrid, and divergence bar chart.
        """

        return {
            "line_chart":
            self.transform_for_line_chart(PROFITABILITY_LINE_METRICS.value),
            "divergence_chart":
            self.transform_for_complex_chart(
                PROFITABILITY_MARGIN_LINE_METRIC.value),
            "bar_chart":
            self.transform_for_bar_chart(PROFITABILITY_LINE_METRICS.value),
            "data_grid":
            self.transform_data_for_datagrid(),
        }
