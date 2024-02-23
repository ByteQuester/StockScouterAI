# Preprocessing and Processing Stages

## Overview

This documentation outlines the initial stages in the data handling pipeline, specifically focusing on preprocessing raw data fetched from the SEC API and processing it into a structured format ready for further **analysis**, **transformation**, or **storage**. These stages are pivotal in populating the base dataframe that feeds into all subsequent analysis and visualization layers, known as the _Base Production Line_.

## Preprocessing Stage

The preprocessing stage is responsible for the initial handling of raw data, preparing it for detailed analysis.

### DataPreprocessor Class

Handles the preprocessing of raw data based on defined metrics and manages the storage or upload of processed data.

| Method                | Description                                                    | Scalability Step         |
|-----------------------|----------------------------------------------------------------|--------------------------|
| preprocess_data       | Preprocesses raw data using annual and quarterly data processors. | Initial Data Preparation |
| _process_data         | Processes data for a given category using the appropriate processor. | Category-Specific Processing |
| _store_or_upload_data | Stores or uploads preprocessed data based on storage preferences. | Data Storage Management  |

## Processing Stage

Following preprocessing, the data undergoes further processing to refine and structure it for analysis or visualization.

### DataProcessor Class

Manages processing and storage of preprocessed data into a csv format optimised for **Second Tier View** as well as the **Chatbot**'s engine, running specific queries and ensuring results are stored or logged accurately.

| Method                    | Description                                                     | Scalability Step           |
|---------------------------|-----------------------------------------------------------------|----------------------------|
| process_and_store_data    | Processes and stores data based on specific queries.             | Query-Based Data Handling |
| _store_and_log_data       | Stores query results in appropriate formats and logs operations. | Result Management and Logging |



## Transformation 
Module manager for processing and stroage of processed data into JSON format optimised for **Third Tier View**. For more comprehensive detail go to [~/app/services/functions/transformers/README.md]()

