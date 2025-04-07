from datetime import datetime, timedelta

import requests

from .utils import get_asset
from .exceptions import GHApiError

def update_gh_status(token:str, status: str, emoji: str):
    query = get_asset('gql/update_status.gql')
    url = 'https://api.github.com/graphql'

    data = {
        'query': query,
        'variables': {
            "msg": status,
            "emoji": f':{emoji}:',
            "expiresAt": (datetime.now() + timedelta(hours=2)).isoformat()
        }
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        raise GHApiError((response.status_code, response.json()))

    return response.json()
