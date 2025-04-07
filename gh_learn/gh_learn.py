import sys
import random
from pprint import pprint

from .auth import GHLogin
from .update_gh_status import update_gh_status
from .exceptions import GHApiError, AuthenticationFailure

def main():
    try:
        token = GHLogin().token
        topics = ' '.join(sys.argv[1:])
        print('Learning:', topics)
        emojis = 'mag', 'notebook', 'bulb', 'mortar_board', 'book'

        resp = update_gh_status(token, f'Learning {topics}', random.choice(emojis))
        print(resp)
    except GHApiError as err:
        print('Request failed with status code:', err)
    except KeyboardInterrupt:
        print('\nbye')
    except AuthenticationFailure as err:
        print('Authentication Error\nDetails:')
        pprint(err.args[0])
