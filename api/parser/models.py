from .utils import db
from .fields import FieldFactory


class ModelFactory:
    def __init__(self, model: dict):
        self.model = model

    def create_model(self) -> db.Model:
        class NewModel(db.Model):
            __tablename__ = self.model['name']

            for fieldname, value in self.model['fields'].items():
                locals()[fieldname] = FieldFactory(value).create_field()

        NewModel.__name__ = self.model['name']
        return NewModel
