import requests

from app.services.functions.managers import LoggingManager
from app.services.types import SECEndpoints


class Roster:
    """
    Manages API endpoints and CIK numbers for SEC API interactions.

    Attributes:
        cik (str): The Central Index Key (CIK) number.
        user_agent (str): The user agent string for API requests.
        api_endpoints (dict): Dictionary of API endpoints.
        api_status (dict): Status of each API endpoint.
        logging_manager (LoggingManager): Instance for logging activities.
    """

    def __init__(self, user_agent: str = "your_email@example.com"):
        """
        Initializes the Roster with an optional user agent.

        Args:
            user_agent (str, optional): User agent string for API requests. Defaults to "your_email@example.com".
        """
        self.cik = None
        self.user_agent = user_agent
        self.api_endpoints = {
            "company_tickers": SECEndpoints.COMPANY_TICKERS.full_url(),
            "submissions": SECEndpoints.SUBMISSIONS.full_url(),
            "company_facts": SECEndpoints.COMPANY_FACTS.full_url(),
        }
        self.api_status = {}
        self.logging_manager = LoggingManager()

    def recruit_cik(self, cik: str) -> 'Roster':
        """
        Assigns a CIK number and updates API endpoints accordingly.
        Args:
            cik (str): The CIK number to be assigned.
        Returns:
            Roster: The current Roster instance.
        """
        if not self._validate_cik(cik):
            self.logging_manager.log(f"Invalid CIK format: {cik}", "ERROR")
            return self

        self.cik = cik
        self._update_api_endpoints(cik)
        self.api_status = self._check_api_status()
        return self

    def _update_api_endpoints(self, cik: str):
        """
        Updates API endpoints that require a CIK number.
        Args:
            cik (str): The CIK number to be used for API endpoints.
        """
        for key in ['submissions', 'company_facts']:
            self.api_endpoints[key] = self.api_endpoints[key].format(cik)

    def _check_api_status(self) -> dict:
        """
        Checks the status of each API endpoint.
        Returns:
            dict: The status of each API endpoint.
        """
        status = {}
        for endpoint_name, endpoint_url in self.api_endpoints.items():
            try:
                response = requests.get(
                    endpoint_url, headers={'User-Agent': self.user_agent})
                status_code = response.status_code
                status[
                    endpoint_name] = 'OK' if status_code == 200 else f'Failed (Status Code: {status_code})'
            except Exception as e:
                status[endpoint_name] = f'Error: {str(e)}'
                self.logging_manager.log_error(
                    f"API status check error for {endpoint_name}: {str(e)}",
                    "ERROR")
        return status

    @staticmethod
    def _validate_cik(cik: str) -> bool:
        """
        Validates the format of a CIK number.
        Args:
            cik (str): The CIK number to validate.
        Returns:
            bool: True if the CIK format is valid, False otherwise.
        """
        return isinstance(cik, str) and cik.isdigit() and len(cik) == 10

    # Additional methods for future use
    def get_api_status(self) -> dict:
        """
        Retrieves the status of the API endpoints.
        Returns:
            dict: The status of each API endpoint.
        """
        return self.api_status

    def print_cik(self):
        """
          Prints the current CIK number.
        """
        print("Current CIK: {}".format(self.cik))

    def update_endpoint(self, endpoint_name: str, url: str):
        """
        Updates the URL for a specific API endpoint.
        Args:
            endpoint_name (str): The name of the endpoint to be updated.
            url (str): The new URL for the endpoint.
        """
        if endpoint_name in self.api_endpoints:
            self.api_endpoints[endpoint_name] = url
            self.logging_manager.log(f"Endpoint {endpoint_name} updated",
                                     "INFO")
        else:
            self.logging_manager.log(f"Endpoint {endpoint_name} not found",
                                     "WARNING")

    def update_cik(self, cik: str):
        """
        Updates the CIK number and associated endpoints.
        Args:
            cik (str): The new CIK number to be updated.
        """
        if self._validate_cik(cik):
            self.cik = cik
            self.logging_manager.log(f"CIK updated to {cik}", "INFO")
            self._update_api_endpoints(cik)
        else:
            self.logging_manager.log(f"Invalid CIK format: {cik}", "ERROR")
