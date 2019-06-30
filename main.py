import asyncio

from aiohttp.web import Application, run_app
from gino.ext.aiohttp import Gino

from models import Country, init_db
from resource import GenericResource
from settings import DB_ADDRESS


async def main(loop):

    await init_db()
    db = Gino()
    app = Application(middlewares=[db])

    db.init_app(
        app,
        config={
            'dsn': DB_ADDRESS
        }
    )

    countries = GenericResource('countries', Country)
    countries.register(app.router)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(main(loop))
    run_app(app)
