from typing import Dict, Union

import pandas as pd

from .transformers_base import (AssetsLiabilitiesTransformer,
                                CashFlowTransformer, LiquidityTransformer,
                                ProfitabilityTransformer)


class TransformerManager:

    def __init__(self) -> None:
        self.transformer_classes: Dict[str, type] = {
            "Profitability": ProfitabilityTransformer,
            "Liquidity": LiquidityTransformer,
            "Assets Liabilities": AssetsLiabilitiesTransformer,
            "Cash Flow": CashFlowTransformer
        }

    def transform_data(self, df: pd.DataFrame, category: str,
                       chart_type: str) -> Union[Dict, pd.DataFrame]:
        """
        Transform data based on category and chart type.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be transformed.
            category (str): The data category (e.g., "Profitability", "Liquidity").
            chart_type (str): The desired chart type ("line_chart", "bar_chart", or other).

        Returns:
            Union[Dict, pd.DataFrame]: Transformed data in a format suitable for the specified chart type.
        """
        transformer_class = self.transformer_classes.get(category)
        if not transformer_class:
            raise ValueError("Unsupported category")
        transformer = transformer_class(df)
        if chart_type == 'line_chart':
            return transformer.transform_for_line_chart()
        elif chart_type == 'bar_chart':
            return transformer.transform_for_bar_chart()
        # TODO: add additional chart transformation e.g, transformer.transform_data_for_datagrid
        else:
            return transformer.transform_all()
