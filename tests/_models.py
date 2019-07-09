import sys
from gino import Gino

sys.path.append('..')

from api.settings import DB_ADDRESS


db = Gino()


async def init_db():
    await db.set_bind(DB_ADDRESS)
    await db.gino.create_all()


async def teardown_db():
    await db.gino.drop_all()


class Country(db.Model):
    __tablename__ = '__countries'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(150))


class Author(db.Model):
    __tablename__ = '__authors'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(150))
    bio = db.Column(db.String(1500))
    country_id = db.Column(db.Integer(), db.ForeignKey(Country.id))


class Book(db.Model):
    __tablename__ = '__books'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(300))
    author_id = db.Column(db.Integer(), db.ForeignKey(Author.id))
    description = db.Column(db.String(1500))
    year = db.Column(db.Integer())
