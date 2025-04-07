import sys
import random
from dotenv import load_dotenv

from .auth import GHLogin
from .update_gh_status import update_gh_status

load_dotenv()

def main():
    token = GHLogin().token

    topics = ' '.join(sys.argv[1:])
    print('Learning:', topics)

    emojis = 'mag', 'notebook', 'bulb', 'mortar_board', 'book'

    resp = update_gh_status(token, f'Learning {topics}', random.choice(emojis))
    print(resp)
