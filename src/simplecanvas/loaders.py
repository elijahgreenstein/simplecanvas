import yaml

from pathlib import Path
from simplecanvas.objects import User

def load_user(token_path):
    with open(token_path) as f:
        user = User(f.read().strip())
    return user
