import json
from .models import ModelFactory


class EndpointsParser:
    def __init__(self):
        self.endpoints = self.get_endpoints()
        self.models = self.create_models()

    @staticmethod
    def get_endpoints():
        with open('innerio.json') as cfg:
            config = json.loads(cfg.read())

        return config['endpoints']

    def create_models(self):
        models = []

        for endpoint in self.endpoints:
            models.append(ModelFactory(endpoint).create_model())

        return models
