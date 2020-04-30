import requests
from typing import Dict, Any, List

from best_testrail_client.custom_types import UserID
from best_testrail_client.models.user import User


class TestRailClient:
    def __init__(self, testrail_url: str, login: str, token: str):
        self.token = token
        self.login = login

        if not testrail_url.endswith('/'):
            testrail_url += '/'
        self.base_url = f'{testrail_url}index.php?/api/v2/'

    # Users API
    def get_user(self, user_id: UserID) -> User:
        user_data = self.__request(f'get_user/{user_id}')
        return User.from_json(user_data)

    def get_user_by_email(self, email: UserID) -> User:
        user_data = self.__request(f'get_user_by_email/{email}')
        return User.from_json(user_data)

    def get_users(self) -> List[User]:
        users_data = self.__request('get_users')
        return [User.from_json(user_data) for user_data in users_data]

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
