import asyncio
from gino import Gino

from settings import DB_ADDRESS


db = Gino()


class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(150))


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(150))
    bio = db.Column(db.String(1500))
    country_id = db.Column(db.Integer(), db.ForeignKey(Country.id))


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(300))
    author_id = db.Column(db.Integer(), db.ForeignKey(Author.id))
    description = db.Column(db.String(1500))
    year = db.Column(db.Integer())


async def init_db():
    await db.set_bind(DB_ADDRESS)


async def migrate():
    await db.set_bind(DB_ADDRESS)
    await db.gino.create_all()


if __name__ == '__main__':
    asyncio.run(migrate())
