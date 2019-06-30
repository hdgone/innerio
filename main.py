from aiohttp.web import Application, run_app
from gino.ext.aiohttp import Gino

from models import Country
from resource import GenericResource
from settings import DB_ADDRESS


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


if __name__ == '__main__':
    run_app(app)
