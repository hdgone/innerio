from gino.dialects.asyncpg import JSON
from .utils import db


class FieldFactory:
    """
    Field Factory is used to create Gino db Columns based on user config input
    Input is presented as a python dictionary

    Use create_field as a main method for column creation.
    """

    def __init__(self, field: dict):
        self.field = field

    def create_field(self) -> db.Column:
        types = {
            "Integer": self._create_integer_data,
            "String": self._create_string_data,
            'JSON': self._create_json_data
        }

        args, kwargs = types[self.field['type']]()

        if 'foreign_key' in self.field:
            args.append(db.ForeignKey(self.field['foreign_key']))

        return db.Column(*args, **kwargs)

    def _create_integer_data(self):
        primary_key = self.field.get("primary_key", None)

        if primary_key is not None:
            return [db.Integer()], {'primary_key': primary_key}
        return [db.Integer()], {}

    def _create_string_data(self):
        length = self.field.get('length', 1000)

        return [db.String(length)], {}

    def _create_json_data(self):
        return [JSON], {}
