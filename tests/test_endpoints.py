import json
import sys

import pytest
from aiohttp.web import Application
from gino.ext.aiohttp import Gino

from .conftest import DB_ADDRESS

sys.path.append('..')

from api.resource import GenericResource
from tests._models import Author, Book, Country, init_db, teardown_db

DB_ADDRESS = 'postgresql://admin:pass@localhost:5432/recipes'


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


async def test_get_for_nonexistent_endpoint_returns_404(cli):
    response = await cli.get('/thisprollydoesnotexist')

    assert response.status == 404


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


async def test_get_non_prefetched_list_endpoints_returns_fks(cli):
    """
    Test if a list endpoint without 'with_prefetch: True' returns
    id's of foreign keys' instances
    """

    response = await cli.get('/authors')

    assert response.status == 200
    assert await response.json() == [
        {
            "id": 1,
            "name": "Test Author",
            "bio": "Test BIO",
            "country_id": 1
        },
        {
            "id": 2,
            "name": "Test Author",
            "bio": "Test BIO",
            "country_id": 2
        },
        {
            "id": 3,
            "name": "Test Author",
            "bio": "Test BIO",
            "country_id": 3
        }
    ]


async def test_get_instance_endpoint_returns_200(cli):
    response = await cli.get('/countries/1')

    assert response.status == 200
    assert await response.json() == {"id": 1, "name": "Test Country"}


async def test_get_instance_endpoint_without_id_returns_400(cli):
    """Test if passing anything instead of id in params returns 400"""

    response = await cli.get('countries/test')

    assert response.status == 400
    assert await response.text() == 'Instance id must be an integer'


async def test_post_for_single_instance_returns_201(cli):
    response = await cli.post('/countries',
                              data=json.dumps({"name": "Test Country"}))

    assert response.status == 201
    assert await response.json() == {"id": 4, "name": "Test Country"}


async def test_post_without_data_returns_400(cli):
    response = await cli.post('/countries')

    assert response.status == 400
    assert await response.text() == "You must specify data " \
                                    "along with the request"


async def test_post_with_wrong_data_type_returns_400(cli):
    response = await cli.post('/countries',
                              data=json.dumps({"name": 123}))

    assert response.status == 400
    assert await response.text() == "invalid input for query" \
                                    " argument $1: 123 (expected str, got int)"


async def test_post_with_extra_data_returns_400(cli):
    response = await cli.post('/countries',
                              data=json.dumps({"name": "Test",
                                               "extra": "test"}))

    assert response.status == 400
    assert await response.text() == "Invalid request data. " \
                                    "Possible choices are: name"


async def test_post_for_nonexistent_foreign_key_returns_400(cli):
    response = await cli.post('/authors',
                              data=json.dumps({"name": "test",
                                               "bio": "test",
                                               "country_id": 999}))

    assert response.status == 400
    assert await response.text() == "Key (country_id)=(999) is" \
                                    " not present in table \"__countries\"."


async def test_patch_for_single_instance_returns_204(cli):
    response = await cli.patch('/countries/1',
                               data=json.dumps({"name": "Country Test"}))

    assert response.status == 204


async def test_patch_for_nonexistent_instance_returns_404(cli):
    response = await cli.patch('/countries/99',
                               data=json.dumps({"name": "Country Test"}))

    assert response.status == 404
    assert await response.text() == "Requested object does not exist"


async def test_delete_for_single_instance_returns_200(cli):
    country = await Country.create(name="Test Country")
    response = await cli.delete(f'/countries/{country.id}')

    assert response.status == 200
    assert await response.text() == f'Successfully deleted {country.id}'
