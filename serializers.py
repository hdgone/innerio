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
        data = await self.serialize_list()
        return json.dumps(data, indent=4).encode('utf-8')

    async def serialize_list(self):
        data = []
        tablename = self.query[0].__table__.name

        for instance in self.query:
            od = OrderedDict()

            for field in self.query[0].__table__.columns:
                # remove table prefix for every field in a table
                field = str(field).replace(f'{tablename}.', '')
                od[field] = getattr(instance, field)

            data.append(od)

        return data
