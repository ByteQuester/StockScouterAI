from .service_manager import DataPipelineIntegration


def generate_data_for_cik(cik_number):
    use_snowflake = False
    data_pipeline = DataPipelineIntegration(cik_number, use_snowflake)
    raw_data = data_pipeline.fetch_data()
    data_pipeline.preprocess_data(raw_data)
    data_pipeline.process_and_store_data()
    data_pipeline.transform_and_store_json()
    # Add logic to notify user of success/failure
