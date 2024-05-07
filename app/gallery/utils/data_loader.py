import json
import os

import markdown
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI


class DataLoader:

    def __init__(self, base_dir='data'):
        self.base_dir = base_dir

    def get_available_cik_numbers(self):
        """
        Returns a list of available CIK numbers based on the directory structure.
        """
        cik_numbers = [
            dir_name for dir_name in os.listdir(self.base_dir)
            if os.path.isdir(os.path.join(self.base_dir, dir_name))
        ]
        return cik_numbers

    def get_entity_name(self, cik):
        """
        Returns the entity name for a given CIK number by examining the data.
        """
        # Example: Using the 'Assets_Liabilities' dataset to get the entity name.
        # Adjust the logic if you're using a different dataset or structure.
        file_path = self.construct_csv_file_path(cik, 'Assets_Liabilities')
        if file_path:
            df = pd.read_csv(file_path)
            if not df.empty and 'ENTITY' in df.columns:
                return df['ENTITY'].iloc[0]
        return "Unknown Entity"

    def get_available_query_types(self, cik):
        """
        Returns a list of available query types for a given CIK number.
        """
        index_file_path = os.path.join(self.base_dir, cik, 'processed_data',
                                       'index.md')
        if os.path.exists(index_file_path):
            with open(index_file_path, 'r') as file:
                md_content = file.read()
                md = markdown.Markdown()
                html_content = md.convert(md_content)
                return self._extract_query_types_from_markdown(html_content)
        return []

    @staticmethod
    def _extract_query_types_from_markdown(html_content):
        """
        Extracts query types from the HTML content of the markdown file using BeautifulSoup.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        query_types = [h3.get_text() for h3 in soup.find_all('h3')]
        return query_types

    def construct_directory_path(self, cik, query_type):
        directory_path = os.path.join(self.base_dir, str(cik),
                                      'processed_data', query_type)
        if os.path.isdir(directory_path):
            return directory_path
        else:
            print(f"Directory not found: {directory_path}")
            return None

    def construct_json_file_path(self, cik, query_type, chart_type):
        """
        Construct path to the JSON file for a specific chart type.
        """
        folder_path = os.path.join(self.base_dir, str(cik), 'processed_json',
                                   query_type, chart_type)
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            if files:
                latest_file = max(files,
                                  key=lambda x: os.path.getctime(
                                      os.path.join(folder_path, x)))
                return os.path.join(folder_path, latest_file)
        return None

    def load_json_data_for_chart(self, cik, query_type, chart_type):
        json_file_path = self.construct_json_file_path(cik, query_type,
                                                       chart_type)
        if json_file_path and os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                return json.load(json_file)
        else:
            return None

    def construct_csv_file_path(self, cik, query_type):
        """
        Construct path to the latest CSV file for a specific query type.
        """
        folder_path = os.path.join(self.base_dir, str(cik), 'processed_data',
                                   query_type)
        if os.path.isdir(folder_path):
            csv_files = [
                file for file in os.listdir(folder_path)
                if file.endswith('.csv')
            ]
            if csv_files:
                # Assuming you want the latest CSV file based on creation time
                latest_file = max(csv_files,
                                  key=lambda x: os.path.getctime(
                                      os.path.join(folder_path, x)))
                return os.path.join(folder_path, latest_file)
        return None

    def load_csv_data(self, cik, query_type):
        """
        Load CSV data for a specific query type and CIK.
        """
        csv_file_path = self.construct_csv_file_path(cik, query_type)
        if csv_file_path and os.path.exists(csv_file_path):
            return pd.read_csv(csv_file_path)
        else:
            st.error(
                f"No CSV data found for CIK {cik} and query type {query_type}."
            )
            return pd.DataFrame()  # Return an empty DataFrame as a fallback

    def push_query_engine(self, cik, query_type):
        directory_path = self.construct_directory_path(cik, query_type)
        return self.load_data(directory_path) if directory_path else None

    @st.cache_resource(show_spinner=False)
    def load_data(_self, directory_path):
        """'_self' is used to un-hash the argument"""
        with st.spinner(
                text=
                "Loading and indexing the docs – hang tight! This should take 1-2 minutes."
        ):
            reader = SimpleDirectoryReader(input_dir=directory_path,
                                           recursive=True)
            docs = reader.load_data()
            service_context = ServiceContext.from_defaults(llm=OpenAI(
                model="gpt-3.5-turbo",
                temperature=0.5,
                system_prompt=
                "You're a finance expert given a set of queries. Analyse the data and answer to the user's questions without hallucinating. Please provide a data table in markdown format from the provided financial data for the questions you are asked. Include an explanation of the answer along with the data table and do not hallucinate."
            ))
            index = VectorStoreIndex.from_documents(
                docs, service_context=service_context)
            query_engine = index.as_query_engine()
            return query_engine

    def load_and_filter_data(self, cik, query_type, chart_type, start_date,
                             end_date):
        """
        Loads JSON data for a chart and filters it by the given date range.
        """
        data = self.load_json_data_for_chart(cik, query_type, chart_type)
        if not data:
            return None

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        if chart_type == "line_chart":
            return self.filter_line_by_date(data, start_date, end_date)
        elif chart_type == "divergence_chart":
            return self.filter_line_by_date(data, start_date, end_date)
        elif chart_type == "data_grid":
            return self.filter_grid_by_date(data, start_date, end_date)
        elif chart_type == "bar_chart":
            return self.filter_bar_by_date(data, start_date, end_date)
        else:
            raise ValueError(f"Unknown chart type: {chart_type}")

    @staticmethod
    def filter_line_by_date(data, start_date, end_date):
        """
        Filters the data by a date range.
        """
        filtered_data = []
        for series in data:
            filtered_series = {
                "id":
                series["id"],
                #"color": series["color"],
                "data": [
                    point for point in series["data"]
                    if pd.to_datetime(start_date) <= pd.to_datetime(point["x"])
                    <= pd.to_datetime(end_date)
                ]
            }
            filtered_data.append(filtered_series)
        return filtered_data

    @staticmethod
    def filter_bar_by_date(data, start_date, end_date):
        """
        Filters the bar chart dataset by a date range.
        """
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_data = [
            item for item in data
            if start_date <= pd.to_datetime(item["Date"]) <= end_date
        ]
        return filtered_data

    @staticmethod
    def filter_grid_by_date(data, start_date, end_date):
        """
        Filters the data grid dataset by a date range.
        """
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_data = [
            item for item in data
            if start_date <= pd.to_datetime(item["year"]) <= end_date
        ]
        return filtered_data

    def get_metric_by_selection(self, cik, query_type, chart_type,
                                selected_metrics):
        """
        Filters chart data based on user-selected metrics. Acts as a manager for filtering functionalities.
        For now, it's tailored for line charts, but it can be extended for other chart types.
        """
        data = self.load_json_data_for_chart(cik, query_type, chart_type)
        if data:
            if chart_type in ['line_chart', 'divergence_chart']:
                return self._filter_line_by_selection(data, selected_metrics)
            elif chart_type == 'bar_chart':
                return self._filter_bar_by_selection(data, selected_metrics)
            # Add similar elif for 'datagrid' if needed
        return []

    @staticmethod
    def _filter_line_by_selection(data, selected_metrics):
        return [metric for metric in data if metric["id"] in selected_metrics]

    @staticmethod
    def _filter_bar_by_selection(data, selected_metrics):
        """
        Filters bar chart data based on selected metrics.
        Assumes metric names are embedded in keys like 'METRIC_NAMEValue' and 'METRIC_NAMEColor'.
        """
        filtered_data = []
        for item in data:
            filtered_item = {}
            for metric in selected_metrics:
                value_key = f"{metric}Value"
                color_key = f"{metric}Color"
                if value_key in item and color_key in item:
                    filtered_item[value_key] = item[value_key]
                    filtered_item[color_key] = item[color_key]
            if 'Date' in item:
                filtered_item['Date'] = item['Date']
            if filtered_item:
                filtered_data.append(filtered_item)
        return filtered_data

    @staticmethod
    def extract_unique_metrics_from_bar_data(data):
        metric_names = set()  # Use a set to avoid duplicates
        for item in data:
            for key in item.keys():
                if "Value" in key:  # Assuming all metrics end with "Value" or "Color"
                    metric_name = key.replace("Value", "")
                    metric_names.add(metric_name)
                elif "Color" in key:  # This line could be omitted if "Color" keys are consistent with "Value" keys
                    metric_name = key.replace("Color", "")
                    metric_names.add(metric_name)
        return list(metric_names)
