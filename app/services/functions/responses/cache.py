import time
from typing import Optional

from cachetools import TTLCache


class CacheManager:

    def __init__(self, maxsize: int = 100, ttl: int = 3600) -> None:
        """
        Initialize the CacheManager with a specified size and time-to-live (TTL) for cache entries.

        Parameters:
            maxsize (int, optional): Maximum size of the cache. Defaults to 100.
            ttl (int, optional): Time-to-live for each cache entry in seconds. Defaults to 3600.
        """
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def get(self, key: str) -> Optional[object]:
        """
        Retrieve data from the cache if it exists and is not expired.

        Args:
            key (str): The key to retrieve data from the cache.

        Returns:
            The cached data or None if it does not exist or is expired.
        """
        if key in self.cache:
            cached_data = self.cache[key]
            if cached_data['expiry'] > time.time():
                return cached_data['data']
        return None

    def store(self, key: str, data: object, expiry: int) -> None:
        """
        Store the data in the cache with a specified expiry duration.

        Args:
            key (str): The key to store the data in the cache.
            data (object): The data to be stored.
            expiry (int): The expiry duration in seconds.
        """
        self.cache[key] = {'data': data, 'expiry': time.time() + expiry}

    def refresh(self) -> None:
        """
        Refresh the stored data in the cache after the expiry period.
        """
        for key, cached_data in self.cache.items():
            if cached_data['expiry'] <= time.time():
                del self.cache[key]
