import sys
import random

import requests

from utils import read

def update_status(status: str, emoji: str):
    query = read('update_status.gql')

    url = 'https://api.github.com/graphql'

    data = {
        'query': query,
        'variables': {
            "msg": status,
            "emoji": emoji
        }
    }

    token = read('token')
    headers = {
        "Authorization": f"bearer {token}"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print(response.json())
    else:
        print('Request failed with status code:', response.status_code)
        print(response.json())


if __name__ == '__main__':
    topics = ' '.join(sys.argv[1:])

    emojis = 'mag', 'notebook', 'bulb', 'mortar_board', 'book'

    update_status(topics, random.choice(emojis))
