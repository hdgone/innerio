import sys

import pytest
from aiohttp.web import Application
from gino.ext.aiohttp import Gino

sys.path.append('..')

from api.resource import GenericResource
from api.settings import DB_ADDRESS
from tests._models import Author, Book, Country, init_db, teardown_db


@pytest.fixture
async def cli(loop, aiohttp_client):
    await init_db()

    db = Gino()
    app = Application(middlewares=[db])

    db.init_app(app, config={'dsn': DB_ADDRESS})

    authors = GenericResource('authors', Author)
    books = GenericResource('books', Book)
    countries = GenericResource('countries', Country)

    authors.register(app.router)
    books.register(app.router)
    countries.register(app.router)

    await _create_model_instances()
    yield await aiohttp_client(app)

    await teardown_db()


async def _create_model_instances():
    for _ in range(1, 4):
        country = await Country.create(name='Test Country')
        author = await Author.create(
            name='Test Author',
            bio='Test BIO',
            country_id=country.id
        )
        await Book.create(
            name='Test Book',
            description='Test Description',
            year=2000,
            author_id=author.id
        )


async def test_get_list_endpoint_returns_200(cli):
    response = await cli.get('/countries')

    assert response.status == 200
    assert await response.json() == [
        {
            "id": 1,
            "name": "Test Country"
        },
        {
            "id": 2,
            "name": "Test Country"
        },
        {
            "id": 3,
            "name": "Test Country"
        },
    ]
