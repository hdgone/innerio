import json
from collections import OrderedDict


class ModelSerializer:
    def __init__(self, query):
        self.query = query

    async def to_json(self):
        data = await self.serialize_list()
        return json.dumps(data, indent=4).encode('utf-8')

    async def serialize_list(self):
        return OrderedDict(
            (field, getattr(self.query, field)) for field
            in self.query.__table__.columns
        )
