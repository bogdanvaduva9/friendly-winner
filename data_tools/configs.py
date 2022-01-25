import json


class Config:
    _configs = {}

    def __init__(self):
        self.load_configs()

    def get_configs(self, model_name):
        return self._configs.get(model_name, {})

    def load_configs(self):
        with open(f"data/model_configs.json", 'r', encoding='utf-8') as json_file:
            configs = json.loads(json_file.read())
            self._configs = configs
