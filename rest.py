import json
from inspect import signature

from aiohttp.web import Response, Request
from aiohttp.web import HTTPMethodNotAllowed, HTTPBadRequest, HTTPNotFound

from serializers import ModelSerializer


DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


class Endpoint:
    def __init__(self):
        self.methods = {}

        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name, method):
        self.methods[method_name.upper()] = method

    async def dispatch(self, request: Request):
        method = self.methods.get(request.method.upper())
        if not method:
            raise HTTPMethodNotAllowed('', DEFAULT_METHODS)

        wanted_args = list(signature(method).parameters.keys())
        available_args = request.match_info.copy()
        available_args.update({'request': request})

        unsatisfied_args = set(wanted_args) - set(available_args.keys())
        if unsatisfied_args:
            # Expected match info that doesn't exist
            raise HTTPBadRequest

        return await method(
            **{arg_name: available_args[arg_name] for arg_name in wanted_args}
        )


class ListEndpoint(Endpoint):
    def __init__(self, model):
        super().__init__()
        self.model = model

    async def get(self) -> Response:
        obj_list = await self.model.query.gino.all()

        if not obj_list:
            return Response(
                status=404,
                body=json.dumps({}),
                content_type='application/json'
            )

        data = await ModelSerializer(obj_list).to_json()

        return Response(
            status=200, body=data, content_type='application/json'
        )

    async def post(self, request) -> Response:
        data = await request.json()

        instance = await self.model.create(**data)
        serialized_instance = await ModelSerializer(instance).to_json()

        return Response(
            status=201,
            body=serialized_instance,
            content_type='application/json'
        )
