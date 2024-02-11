# In configs/snowflake_config.py
# noinspection PyUnresolvedReferences
from decouple import config


class SnowflakeConfig:

    def __init__(self):
        self.user = config('SNOWFLAKE__USER')
        self.password = config('SNOWFLAKE__PASSWORD')
        self.account = config('SNOWFLAKE__ACCOUNT')
        self.warehouse = config('SNOWFLAKE__WAREHOUSE')
        self.database = config('SNOWFLAKE__DATABASE')
        self.schema = config('SNOWFLAKE__SCHEMA')
        self.port = config('SNOWFLAKE__PORT', default='443')
        self.role = config('SNOWFLAKE__ROLE', default='ACCOUNTADMIN')
