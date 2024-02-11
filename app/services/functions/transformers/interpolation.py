from datetime import datetime
from typing import Dict, List, Tuple, Union

import pandas as pd


class InterpolationTransformer:
    """
    A class to perform interpolation transformation on financial data, handling transitions between positive and
    negative values of a specified metric. This class segregates data based on the sign of a given metric, identifies
    transition points between positive and negative values, and interpolates data to ensure smooth transitions for
    visualization purposes.

    Attributes:
        data (pd.DataFrame): The dataset to transform, expected to contain datetime and financial metrics columns.

    Example usage:
    >>> data = {
    ...     'ENTITY': ['BOEING CO'] * 13,
    ...     'CIK': [12927] * 13,
    ...     'DATE': ['2014-03-31', '2014-06-30', '2014-09-30', '2014-12-31',
    ...              '2015-03-31', '2015-06-30', '2015-09-30', '2015-12-31',
    ...              '2016-03-31', '2016-06-30', '2016-09-30', '2016-12-31', '2017-03-31'],
    ...     'Year': [2014] * 4 + [2015] * 4 + [2016] * 4 + [2017],
    ...     'Quarter': ['Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4', 'Q1'],
    ...     'PROFIT_MARGIN': [4.72, 7.5, 5.73, 5.99, 6.03, 4.52, 6.59, 4.35, 5.39, -0.95, 9.54, 7.0, 7.19]
    ... }
    >>> df = pd.DataFrame(data)
    >>> df['DATE'] = pd.to_datetime(df['DATE'])
    >>> transformer = InterpolationTransformer(df)
    >>> metric = 'PROFIT_MARGIN'
    >>> interpolated_data = transformer.stream(metric)
    >>> print(interpolated_data)
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the InterpolationTransformer with financial data.

        Args:
            df (pd.DataFrame): The dataset containing financial metrics and dates.
        """
        self.data = df
        #print(self.data.head())

    def segregate_data_by_sign(
            self, metric: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Segregates the dataset into two subsets based on the sign (positive or negative) of the specified metric.

        Args:
            metric (str): The financial metric column based on which to segregate the data.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Two DataFrames, the first containing positive values and the second
            containing negative values of the specified metric.
        """
        #print("Segregating data by sign...")
        positive_mask = self.data[metric] >= 0
        negative_mask = self.data[metric] < 0
        positive_data = self.data[positive_mask]
        negative_data = self.data[negative_mask]
        #print(f"Positive data: {positive_data.head(10)}")
        #print(f"Negative data: {negative_data.head(10)}")
        return positive_data, negative_data

    def find_transition_points(
            self, positive_df: pd.DataFrame,
            negative_df: pd.DataFrame) -> List[Tuple[str, str]]:
        """
        Identifies transition points between positive and negative values of the financial metric.

        Args:
            positive_df (pd.DataFrame): DataFrame containing positive values of the financial metric.
            negative_df (pd.DataFrame): DataFrame containing negative values of the financial metric.

        Returns:
            List[Tuple[str, str]]: A list of tuples, each containing the dates marking the transition from positive to negative or vice versa.
        """
        #print("Finding transition points...")
        transition_points = []

        # Ensure dataframes are sorted by date
        positive_df = positive_df.sort_values(by='DATE')
        negative_df = negative_df.sort_values(by='DATE')

        # Combine and sort all unique dates from both dataframes
        all_dates = pd.concat([positive_df['DATE'], negative_df['DATE']
                               ]).drop_duplicates().sort_values()

        # Iterate through all dates, checking for transitions
        for i in range(len(all_dates) - 1):
            current_date = all_dates.iloc[i]
            next_date = all_dates.iloc[i + 1]

            # Check if current date is in positive and next date is in negative, or vice versa
            current_in_positive = current_date in positive_df['DATE'].values
            current_in_negative = current_date in negative_df['DATE'].values
            next_in_positive = next_date in positive_df['DATE'].values
            next_in_negative = next_date in negative_df['DATE'].values

            # If transition from positive to negative
            if current_in_positive and next_in_negative:
                transition_points.append((current_date, next_date))
            # If transition from negative to positive
            elif current_in_negative and next_in_positive:
                transition_points.append((current_date, next_date))

        return transition_points

    def ensure_corresponding_entries(
            self, positive_df: pd.DataFrame,
            negative_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Ensure each DataFrame has an entry for each date in the combined set of dates, filling missing entries with None.

        Args:
            positive_df (pd.DataFrame): DataFrame with positive values of the metric.
            negative_df (pd.DataFrame): DataFrame with negative values of the metric.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: The updated positive and negative DataFrames with consistent date entries.
        """
        #print("Ensuring corresponding entries...")
        all_dates = pd.concat([positive_df['DATE'],
                               negative_df['DATE']]).unique()

        # Ensure both DataFrames have entries for all dates, filling with NaN where data is missing
        # This can be done by reindexing each DataFrame based on the full date range
        full_date_range = pd.DataFrame(all_dates,
                                       columns=['DATE']).sort_values(by='DATE')

        positive_df = full_date_range.merge(positive_df, on='DATE',
                                            how='left').fillna({'y': None})
        negative_df = full_date_range.merge(negative_df, on='DATE',
                                            how='left').fillna({'y': None})

        return positive_df, negative_df

    def calculate_transition_date(self, start_date: str, end_date: str) -> str:
        """
        Calculates the midpoint date between two dates, used as a transition point.

        Args:
            start_date (str): The starting date of the transition period.
            end_date (str): The ending date of the transition period.

        Returns:
            str: The calculated midpoint date as a string.
        """
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        midpoint = start_date_obj + (end_date_obj - start_date_obj) / 2
        return midpoint.strftime('%Y-%m-%d')

    def insert_zero_entry(
            self, df: pd.DataFrame, metric: str,
            transition_dates: List[Tuple[str, str]]) -> pd.DataFrame:
        """
        Inserts zero entries into the dataset at specified transition dates for smooth interpolation.

        Args:
            df (pd.DataFrame): The DataFrame to modify.
            metric (str): The financial metric column to update with zero values at transition points.
            transition_dates (List[Tuple[str, str]]): Transition dates where zero entries should be inserted.

        Returns:
            pd.DataFrame: The modified DataFrame with zero entries added at transition points.
        """
        #print("Inserting zero entries...")
        new_entries = [{
            'DATE': self.calculate_transition_date(start, end),
            metric: 0
        } for start, end in transition_dates]
        new_entries_df = pd.DataFrame(new_entries)
        return pd.concat([df, new_entries_df],
                         ignore_index=True).sort_values(by='DATE')

    def synchronize_dataframes(
            self, positive_df: pd.DataFrame, negative_df: pd.DataFrame,
            metric: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Synchronizes positive and negative DataFrames to ensure each contains entries for all dates present in either DataFrame.

        Args:
            positive_df (pd.DataFrame): DataFrame containing positive values.
            negative_df (pd.DataFrame): DataFrame containing negative values.
            metric (str): The financial metric being processed.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: The synchronized positive and negative DataFrames.
        """
        #print("Synchronizing dataframes...")
        # Combine all unique dates from both DataFrames and sort them
        all_dates = pd.concat([
            positive_df['DATE'], negative_df['DATE']
        ]).drop_duplicates().sort_values().reset_index(drop=True)

        # Convert 'DATE' columns in both dataframes to string format if not already to ensure matching formats
        positive_df['DATE'] = positive_df['DATE'].astype(str)
        negative_df['DATE'] = negative_df['DATE'].astype(str)

        # Create a DataFrame from all_dates to ensure no duplicates and proper indexing
        all_dates_df = pd.DataFrame({'DATE': all_dates}).drop_duplicates()

        # Merge with all_dates_df to ensure each dataframe has an entry for each date
        positive_synced = all_dates_df.merge(positive_df,
                                             on='DATE',
                                             how='left')
        negative_synced = all_dates_df.merge(negative_df,
                                             on='DATE',
                                             how='left')

        # Fill NaN values for the metric with None
        positive_synced[metric] = positive_synced[metric].where(
            pd.notnull(positive_synced[metric]), None)
        negative_synced[metric] = negative_synced[metric].where(
            pd.notnull(negative_synced[metric]), None)

        # Optionally, if other columns should also be filled with forward values, apply ffill and bfill
        columns_to_fill = ['ENTITY', 'CIK', 'Year',
                           'Quarter']  # Add or remove columns as needed
        for col in columns_to_fill:
            positive_synced[col] = positive_synced[col].ffill().bfill(
            ).infer_objects()
            negative_synced[col] = negative_synced[col].ffill().bfill(
            ).infer_objects()

        return positive_synced, negative_synced

    def transform_dataframe_to_json_like(
        self, df: pd.DataFrame, metric: str, series_id: str
    ) -> Dict[str, Union[str, List[Dict[str, Union[str, float]]]]]:
        """
        Transforms a DataFrame into a JSON-like structure for visualization purposes.

        Args:
            df (pd.DataFrame): The DataFrame to transform.
            metric (str): The financial metric to include in the transformation.
            series_id (str): A unique identifier for the data series.

        Returns:
            Dict: A JSON-like structure representing the transformed data.
        """
        #print("Transforming dataframe to JSON-like structure...")
        data_series = []
        for index, row in df.iterrows():
            # Ensure 'DATE' is processed correctly
            try:
                x_value = row['DATE'] if isinstance(
                    row['DATE'], str) else pd.to_datetime(
                        row['DATE']).strftime('%Y-%m-%d')
            except Exception as e:
                print(f"Error processing DATE at index {index}: {e}")
                x_value = None

            # Ensure 'y' value is processed correctly, avoiding Series ambiguity
            try:
                y_value = row[metric] if pd.notna(row[metric]) else None
            except Exception as e:
                print(
                    f"Error processing metric {metric} at index {index}: {e}")
                y_value = None

            data_series.append({"x": x_value, "y": y_value})

        return {"data": data_series, "id": series_id}

    def stream(self, metric: str) -> List[Dict]:
        """
        Performs the entire transformation process and returns a list of JSON-like structures for both positive and negative data series.

        Args:
            metric (str): The financial metric to process.

        Returns:
            List[Dict]: A list containing JSON-like structures for positive and negative data series.
        """
        #print(f"Streaming data for metric: {metric}")
        try:
            positive_d, negative_d = self.segregate_data_by_sign(metric)
            transition_dates = self.find_transition_points(
                positive_d, negative_d)
            positive_df, negative_df = self.ensure_corresponding_entries(
                positive_d, negative_d)
            positive_df_with_zeros = self.insert_zero_entry(
                positive_df, metric, transition_dates)
            negative_df_with_zeros = self.insert_zero_entry(
                negative_df, metric, transition_dates)
            positive_df_s, negative_df_s = self.synchronize_dataframes(
                positive_df_with_zeros, negative_df_with_zeros, metric)
            positive_json = self.transform_dataframe_to_json_like(
                positive_df_s, metric, f"{metric} positive")
            negative_json = self.transform_dataframe_to_json_like(
                negative_df_s, metric, f"{metric} negative")
            return [positive_json, negative_json]
        except Exception as e:
            print(f"Error during stream processing for metric {metric}: {e}")
            return []


"""
# Example usage
import pandas as pd
data = {
    'ENTITY': ['BOEING CO'] * 13,
    'CIK': [12927] * 13,
    'DATE': ['2014-03-31', '2014-06-30', '2014-09-30', '2014-12-31',
             '2015-03-31', '2015-06-30', '2015-09-30', '2015-12-31',
             '2016-03-31', '2016-06-30', '2016-09-30', '2016-12-31', '2017-03-31'],
    'Year': [2014] * 4 + [2015] * 4 + [2016] * 5,
    'Quarter': ['Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4', 'Q1'],
    'NET_INCOME_LOSS': [965.0, 1653.0, 1362.0, 1466.0, 1336.0, 1110.0, 1704.0, 1026.0,
                        1219.0, -234.0, 2279.0, 1631.0, 1579.0],
    'OPS_INCOME_LOSS': [1542.0, 1787.0, 2119.0, 2025.0, 2019.0, 1683.0, 2580.0, 1161.0,
                        1788.0, -419.0, 2282.0, 2183.0, 2206.0],
    'REVENUES': [20465.0, 22045.0, 23784.0, 24468.0, 22149.0, 24543.0, 25849.0, 23573.0,
                 22632.0, 24755.0, 23898.0, 23286.0, 21961.0],
    'PROFIT_MARGIN': [4.72, 7.5, 5.73, 5.99, 6.03, 4.52, 6.59, 4.35, 5.39, -0.95, 9.54, 7.0, 7.19]
}
df = pd.DataFrame(data)
transformer = InterpolationTransformer(df)
metric = 'PROFIT_MARGIN'
interpolated_data = transformer.stream(metric)
"""
