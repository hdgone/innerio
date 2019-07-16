import asyncio

from api.settings import DB_ADDRESS
from api.parser.endpoints_parser import EndpointsParser
from api.parser.utils import db


models_collection = EndpointsParser().models


async def init_db():
    await db.set_bind(DB_ADDRESS)


async def migrate():
    await db.set_bind(DB_ADDRESS)
    await db.gino.create_all()


if __name__ == '__main__':
    asyncio.run(migrate())
