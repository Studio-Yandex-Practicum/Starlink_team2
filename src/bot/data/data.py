import json
import pathlib

base_dir = pathlib.Path(__file__).parent.parent

with open(base_dir / 'data/emails.json') as f:
    EMAILS = json.load(f)

with open(base_dir / 'data/roles.json') as f:
    ROLES = json.load(f)

with open(base_dir / 'data/menus.json') as f:
    MENUS = json.load(f)
