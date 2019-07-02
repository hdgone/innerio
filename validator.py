from asyncpg.exceptions import DataError
from aiohttp.web import HTTPBadRequest, HTTPNotFound


class Validator:
    """
    Data validator class which executes on top of GINO's CRUD methods with
    validation before execution.

    :param model: a GINO model to execute methods on
    """
    def __init__(self, model):
        self.model = model

    async def retrieve_all(self):
        obj_list = await self.model.query.gino.all()

        if not obj_list:
            raise HTTPNotFound()

        return obj_list

    async def create(self, **kwargs):

        if not kwargs:
            raise HTTPBadRequest(text="Request body cannot be empty.")

        try:
            instance = await self.model.create(**kwargs)
        except KeyError:
            raise HTTPBadRequest(
                text=f"Invalid request data. Possible choices are: "
                     f"{', '.join(self._get_table_columns())}"
            )
        except DataError as e:
            raise HTTPBadRequest(text=str(e))
        else:
            return instance

    def _get_table_columns(self):
        tablename = self.model.__table__.name
        columns = []

        for column in self.model.__table__.columns:
            col = str(column).replace(f'{tablename}.', '')
            if col != 'id':
                columns.append(col)

        return columns
