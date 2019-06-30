import json
from collections import OrderedDict


class ModelSerializer:
    """
    :param query: query set with a fetched model
    :return json-representation of a given queryset
    """
    def __init__(self, query):
        self.query = query

    async def to_json(self):
        if isinstance(self.query, list):
            data = await self.serialize_list()
        else:
            data = await self.serialize_instance()
        return json.dumps(data, indent=4).encode('utf-8')

    async def serialize_instance(self):
        """Serialize a single model instance"""

        tablename = self.query.__table__.name
        return await self._create_instance_dict(instance=self.query,
                                                tablename=tablename)

    async def serialize_list(self):
        """Serialize a list of model instances"""

        data = []
        tablename = self.query[0].__table__.name

        for instance in self.query:
            od = await self._create_instance_dict(instance=instance,
                                                  tablename=tablename)
            data.append(od)

        return data

    @staticmethod
    async def _create_instance_dict(
            instance, tablename, input_dict=None
    ):
        if input_dict is None:
            input_dict = OrderedDict()

        for field in instance.__table__.columns:
            # remove table prefix for every field in a table
            field = str(field).replace(f'{tablename}.', '')
            input_dict[field] = getattr(instance, field)

        return input_dict
