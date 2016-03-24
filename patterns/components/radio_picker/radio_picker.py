import json
from patterns.base_component import BaseComponent

with './config.json' as file:
    DEFAULT = json.load(file)


class RadioPicker(BaseComponent):
    pass
