from os import path

def read(f_name: str):
    f_name = path.join(path.dirname(__file__), f_name)

    if not path.isfile(f_name):
        return None

    with open(f_name, 'r') as f:
        return f.read()
