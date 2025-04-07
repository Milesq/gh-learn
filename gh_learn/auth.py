from os import environ, path
import requests

from .utils import get_asset

LOGIN_DEVICE_CODE_URL = 'https://github.com/login/device/code'
ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

class GHLogin:
    def __init__(self):
        self.token = get_asset('token')
        if self.token is None:
            self.login()

    def login(self):
        headers = {
            'Accept': 'application/json'
        }

        data = {
            'client_id': environ['GH_CLIENT_ID'],
            'scope': 'user',
        }

        resp = requests.post(
            LOGIN_DEVICE_CODE_URL,
            data=data,
            headers=headers
        ).json()

        device_code = resp['device_code']

        print('Token is missing. Login to GitHub, pase the code below and press Enter')
        print(resp['verification_uri'])
        print('Code: ', resp['user_code'])

        input()

        data = {
            'client_id': environ['GH_CLIENT_ID'],
            'device_code': device_code,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
        }

        resp = requests.post(
            ACCESS_TOKEN_URL,
            data=data,
            headers=headers
        ).json()

        print(resp)

        self.token = resp.get('access_token')

        if not self.token:
            print('Failed to login')
            print(resp)
            exit(1)

        self.write_token()

    def write_token(self):
        f_name = path.join(path.dirname(), 'token')

        with open(f_name, 'w') as f:
            f.write(self.token)
