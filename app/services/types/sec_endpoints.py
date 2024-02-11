from enum import Enum


class SECEndpoints(Enum):
    BASE_URL = "https://data.sec.gov"
    COMPANY_TICKERS = "/files/company_tickers.json"
    SUBMISSIONS = "/submissions/CIK{}.json"
    COMPANY_FACTS = "/api/xbrl/companyfacts/CIK{}.json"

    def full_url(self, cik=None):
        url = "https://www.sec.gov" + self.value if self == SECEndpoints.COMPANY_TICKERS else f'{self.BASE_URL.value}{self.value}'
        return url.format(cik) if cik else url
