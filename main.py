import sys
import random
from datetime import datetime, timedelta

import requests

from login import GHLogin
from utils import read
from dotenv import load_dotenv

load_dotenv()

def update_gh_status(status: str, emoji: str):
    query = read('update_status.gql')

    url = 'https://api.github.com/graphql'

    data = {
        'query': query,
        'variables': {
            "msg": status,
            "emoji": f':{emoji}:',
            "expiresAt": (datetime.now() + timedelta(hours=2)).isoformat()
        }
    }

    token = read('token')
    headers = {
        "Authorization": f"bearer {token}"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        print('Request failed with status code:', response.status_code)

    print(response.json())


if __name__ == '__main__':
    token = GHLogin().token

    topics = ' '.join(sys.argv[1:])

    emojis = 'mag', 'notebook', 'bulb', 'mortar_board', 'book'

    update_gh_status(f'Learning {topics}', random.choice(emojis))
