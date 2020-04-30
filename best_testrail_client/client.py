import requests
from typing import Dict, Any


class TestRailClient:
    def __init__(self, testrail_url: str, login: str, token: str):
        self.token = token
        self.login = login

        if not testrail_url.endswith('/'):
            testrail_url += '/'
        self.base_url = f'{testrail_url}index.php?/api/v2/'

    def __request(
        self, url: str, data: Dict = None, method: str = 'GET',
        _return_json: bool = True,
    ) -> Any:
        if data is None:
            data = {}

        response = requests.request(
            method, f'{self.base_url}{url}', json=data,
            auth=(self.login, self.token),
        )

        if _return_json:
            return response.json()
        return response
