import asyncio
import time

import sys
sys.path.append('/')

from settings import DB_ADDRESS

from parser.endpoints_parser import EndpointsParser
from parser.utils import db


models_collection = EndpointsParser().models


async def init_db():
    await db.set_bind(DB_ADDRESS)


async def migrate():
    await db.set_bind(DB_ADDRESS)
    await db.gino.create_all()


if __name__ == '__main__':
    try:
        asyncio.run(migrate())
    except ConnectionRefusedError:
        print('database connection refused, retrying in 5 seconds...')
        time.sleep(5)
        asyncio.run(migrate())
