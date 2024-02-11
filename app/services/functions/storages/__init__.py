# In services/functions/storages/__init__.py

from .local_data_storage import DataStorageManager
from .sw_flake import SnowflakeDataManager

__all__ = ['SnowflakeDataManager', 'DataStorageManager']
