# Assuming this structure for your tests:
# tests/unit/functions/responses/test_sec_api_client.py
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from app.services.functions import SECAPIClient


class TestSECAPIClient(unittest.TestCase):
    @patch('app.services.functions.responses.sec_api_client.requests.get')
    @patch('app.services.functions.responses.sec_api_client.CacheManager')
    def test_fetch_company_tickers(self, mock_cache, mock_get):
        # Setup: Prepare mock responses
        mock_response = MagicMock()
        mock_response.json.return_value = {
            # Populate this dict with a sample response from your expected API call
        }
        mock_response.status_code = 200
        mock_response.headers = {
            'X-RateLimit-Remaining': '100',
            'X-RateLimit-Reset': '123456789'
        }
        mock_get.return_value = mock_response

        # Initialize SECAPIClient with mocked CacheManager
        client = SECAPIClient()

        # Exercise: Call the method under test
        result = client.fetch_company_tickers()

        # Verify: Ensure the method behaves as expected with the mocked response
        self.assertIsInstance(result, pd.DataFrame)
        # Add more assertions based on the expected structure of your DataFrame

        # Verify that requests.get was called with the correct URL
        mock_get.assert_called_with(client.base_url + "/path/to/company/tickers", headers=ANY)

        # Cleanup: Not necessary for this test

if __name__ == '__main__':
    unittest.main()
