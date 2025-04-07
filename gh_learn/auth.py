import requests
import keyring

from .exceptions import AuthenticationFailure
from .config import GH_CLIENT_ID

LOGIN_DEVICE_CODE_URL = 'https://github.com/login/device/code'
ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

class GHLogin:
    def __init__(self):
        self.token = self.read_token()

        if self.token is None:
            self.login()

    headers = {
        'Accept': 'application/json'
    }

    def login(self):
        data = {
            'client_id': GH_CLIENT_ID,
            'scope': 'user',
        }

        resp = requests.post(
            LOGIN_DEVICE_CODE_URL,
            data=data,
            headers=self.headers
        ).json()

        device_code = resp.get('device_code')

        if not device_code:
            raise AuthenticationFailure(resp)

        print('Token is missing. Login to GitHub, pase the code below and press Enter')
        print(resp['verification_uri'])
        print('Code: ', resp['user_code'])

        input()

        self.__finish_login(device_code)

    def __finish_login(self, device_code):
        data = {
            'client_id': GH_CLIENT_ID,
            'device_code': device_code,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
        }

        resp = requests.post(
            ACCESS_TOKEN_URL,
            data=data,
            headers=self.headers
        ).json()

        self.token = resp.get('access_token')

        if not self.token:
            if resp.get('error') == 'authorization_pending':
                input("It seems you didn't login yet. Press Enter once you do it\n")
                return self.__finish_login(device_code)

            raise AuthenticationFailure(resp)

        self.write_token()

    def write_token(self):
        keyring.set_password('dev.milesq.gh-learn', 'default', self.token)

    def read_token(self):
        return keyring.get_password('dev.milesq.gh-learn', 'default')

