import asyncio

from aiohttp.web import Application, run_app
from gino.ext.aiohttp import Gino

from api.models import models_collection, init_db
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

    for model in models_collection:
        resource = GenericResource(model.__table__.name, model)
        resource.register(app.router)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(main(loop))
    run_app(app, host='0.0.0.0', port=8080)
