import asyncio

from aiohttp.web import Application, run_app
from gino.ext.aiohttp import Gino

from api.models import Author, Country, init_db
from api.resource import GenericResource
from api.settings import DB_ADDRESS


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
    authors = GenericResource('authors', Author)
    countries.register(app.router)
    authors.register(app.router)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(main(loop))
    run_app(app)
