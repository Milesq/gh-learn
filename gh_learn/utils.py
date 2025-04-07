from os import path
from importlib.resources import files

def get_asset(f_name: str):
    f_name = files('gh_learn').joinpath(f_name)
    if not path.isfile(f_name):
        return None

    with open(f_name, 'r') as f:
        return f.read()
