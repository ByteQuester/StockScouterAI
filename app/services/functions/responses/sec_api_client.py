import time
from datetime import datetime
from typing import Any, Dict, Optional, Union

import pandas as pd
import requests
from cachetools import TTLCache

from app.services.functions.managers import LoggingManager
from app.services.types import BASE_URL
from app.services.utils import Roster

from .cache import CacheManager


class SECAPIClient:

    def __init__(self, base_url: Optional[str] = None) -> None:
        """
        Initialize SECAPIClient with an optional base URL. Uses default if not provided.

        Args:
            base_url (str, optional): Base URL for the SEC API. Defaults to BASE_URL.
        """
        self.base_url = base_url if base_url else BASE_URL
        self.error_handler = LoggingManager()
        self.rate_limit: Optional[Dict[str, int]] = None
        self.cache = CacheManager(maxsize=100, ttl=3600)  # Cache for 1 hour
        self.roster = Roster()

    def fetch_company_tickers(self) -> Union[pd.DataFrame, Dict[str, Any]]:
        """
        Fetch and return company tickers from the SEC API. Uses cache if available.

        Returns:
            pd.DataFrame or dict: Parsed tickers data or error information.
        """
        key = 'company_tickers'
        cached_response = self.cache.get(key)
        if cached_response:
            return self._parse_response(cached_response, 'tickers')

        url = self.roster.api_endpoints["company_tickers"]
        response = self._send_get_request(url)
        if response:
            self.cache.store(key, response, expiry=3600)

            parsed_data = self._parse_response(response, 'tickers')
            if isinstance(parsed_data, pd.DataFrame):
                return parsed_data
            else:
                return {'error': 'Failed to parse company tickers'}

        return {'error': 'Failed to fetch company tickers'}

    def fetch_submissions(
            self, cik_number: str) -> Union[pd.DataFrame, Dict[str, Any]]:
        """
        Fetch submissions for a given CIK number. Uses cache if available.

        Parameters:
            cik_number (str): CIK number of the company.

        Returns:
            pd.DataFrame or dict: Parsed submissions data or error information.
        """
        key = f'submissions_{cik_number}'
        cached_data = self.cache.get(key)
        if cached_data:
            return cached_data
        url = self.roster.recruit_cik(cik_number).api_endpoints["submissions"]
        response = self._send_get_request(url)
        if response:
            self.cache.store(key, response, expiry=3600)

            parsed_data = self._parse_response(response, 'submissions')
            if isinstance(parsed_data, pd.DataFrame):
                return parsed_data
            else:
                return {'error': 'Failed to parse company submissions'}

    def fetch_company_facts(
            self, cik_number: str) -> Union[pd.DataFrame, Dict[str, Any]]:
        """
        Fetch facts about a company using its CIK number. Uses cache if available.

        Parameters:
            cik_number (str): CIK number of the company.

        Returns:
            pd.DataFrame or dict: Parsed company facts data or error information.
        """
        key = f'company_facts_{cik_number}'
        cached_response = self.cache.get(key)
        if cached_response:
            return self._parse_response(cached_response, 'company_facts')

        url = self.roster.recruit_cik(
            cik_number).api_endpoints["company_facts"]
        response = self._send_get_request(url)
        if response:
            self.cache.store(key, response, expiry=3600)  # Cache for 1 hour

            parsed_data = self._parse_response(response, 'company_facts')
            if isinstance(parsed_data, pd.DataFrame):
                return parsed_data
            else:
                return {'error': 'Failed to parse company facts'}

        return {'error': 'Failed to fetch company facts'}

    def _send_get_request(self, url: str) -> Union[Dict[str, Any], None]:
        """
        Send a GET request to the SEC API.
        Args:
            url (str): The URL of the API endpoint.
        Returns:
            dict or None: The response from the API as a JSON object, or None if there was a parsing error.
        """
        # TBD dynamic handling of 'User-Agent' based on user's input
        headers = {'User-Agent': 'YourName <your_email@example.com>'}
        try:
            if self.rate_limit and self.rate_limit['remaining'] == 0:
                cooldown_period = self.rate_limit['reset'] - time.time()
                if cooldown_period > 0:
                    time.sleep(cooldown_period +
                               1)  # Add an extra second to cooldown period
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if 'X-RateLimit-Remaining' in response.headers:
                self.rate_limit = {
                    'remaining':
                    int(response.headers['X-RateLimit-Remaining']),
                    'reset': int(response.headers['X-RateLimit-Reset'])
                }
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Error sending GET request: {str(e)}"
            self.error_handler.log_error(error_message)
            return {'error': error_message}
        except Exception as e:
            error_message = f"Error during API request: {str(e)}"
            self.error_handler.log_error(error_message)
            return {'error': error_message}

    def _parse_response(self, response: Dict[str, Any],
                        response_type: str) -> Union[pd.DataFrame, None]:
        """
        Parse the raw JSON response based on the type of data.
        Args:
            response (dict): The raw JSON response from the SEC API.
            response_type (str): The type of data (e.g., 'tickers', 'submissions', 'company_facts').
        Returns:
            pd.DataFrame or None: The parsed response as a DataFrame, or None in case of error.
        """
        try:
            if response_type == 'tickers':
                # TBD Specific parsing logic for tickers (consider maybe separating the methods below?)
                pass
            elif response_type == 'submissions':
                # TBD Specific parsing logic for submissions
                pass
            elif response_type == 'company_facts':
                entityname, cik = response['entityName'], response['cik']
                all_flattened_data = []
                current_year = datetime.now().year
                ten_years_ago = current_year - 10
                for metric_key, metric_data in response['facts'][
                        'us-gaap'].items():
                    if 'units' in metric_data and 'USD' in metric_data['units']:
                        usd_data = metric_data['units']['USD']

                        flattened_data = [{
                            'EntityName': entityname,
                            'CIK': cik,
                            'Metric': metric_key,
                            **item
                        } for item in usd_data if datetime.strptime(
                            item['end'], '%Y-%m-%d').year >= ten_years_ago]
                        all_flattened_data.extend(flattened_data)

                return pd.DataFrame(all_flattened_data)
            else:
                self.error_handler.log_error(
                    f"Unknown response type: {response_type}")
                return None
        except Exception as e:
            self.error_handler.log_error(f"Error parsing response: {str(e)}")
            return None
