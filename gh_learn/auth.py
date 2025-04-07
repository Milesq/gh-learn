from os import path
from importlib.resources import files

import requests
from dotenv import dotenv_values

from .utils import get_asset
from .exceptions import AuthenticationFailure

LOGIN_DEVICE_CODE_URL = 'https://github.com/login/device/code'
ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

class GHLogin:
    def __init__(self):
        dotenv_path = files('gh_learn').joinpath('.public.env')
        config = dotenv_values(dotenv_path)

        self.gh_client_id = config['GH_CLIENT_ID']
        self.token = get_asset('token')
        if self.token is None:
            self.login()

    headers = {
            'Accept': 'application/json'
    }

    def login(self):
        data = {
            'client_id': self.gh_client_id,
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
            'client_id': self.gh_client_id,
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
        f_name = path.join(path.dirname(), 'token')

        with open(f_name, 'w') as f:
            f.write(self.token)
