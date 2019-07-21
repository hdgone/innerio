from inspect import signature

from aiohttp.web import Response, Request
from aiohttp.web import HTTPMethodNotAllowed, HTTPBadRequest

from api.serializers import ModelSerializer
from api.validator import Validator


ALLOWED_HEADERS = ('Content-Type', 'Access-Control-Allow-Headers',
                           'Authorization', 'X-Requested-With')
DEFAULT_METHODS = ('GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS')
DEFAULT_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': ', '.join(DEFAULT_METHODS),
    'Access-Control-Allow-Headers': ', '.join(ALLOWED_HEADERS)
}


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

    async def options(self, request):

        return Response(
            status=200,
            headers=DEFAULT_HEADERS
        )


class ListEndpoint(Endpoint):
    def __init__(self, model):
        super().__init__()
        self.validator = Validator(model)

    async def get(self) -> Response:
        obj_list = await self.validator.retrieve_all()

        data = await ModelSerializer(obj_list).to_json()

        return Response(
            status=200,
            body=data,
            content_type='application/json',
            headers=DEFAULT_HEADERS
        )

    async def post(self, request) -> Response:
        data = await self.validator.validate_request_data(request)

        instance = await self.validator.create(**data)
        serialized_instance = await ModelSerializer(instance).to_json()

        return Response(
            status=201,
            body=serialized_instance,
            content_type='application/json',
            headers=DEFAULT_HEADERS
        )


class InstanceEndpoint(Endpoint):
    def __init__(self, model):
        super().__init__()
        self.validator = Validator(model)

    async def get(self, instance_id):
        instance = await self.validator.retrieve(instance_id)
        data = await ModelSerializer(instance).to_json()

        return Response(
            status=200,
            body=data,
            content_type='application/json',
            headers=DEFAULT_HEADERS
        )

    async def patch(self, request, instance_id):
        request_data = await self.validator.validate_request_data(request)
        await self.validator.update(instance_id, **request_data)

        return Response(status=204, headers=DEFAULT_HEADERS)

    async def delete(self, instance_id):
        await self.validator.delete(instance_id)

        return Response(
            status=200,
            text=f'Successfully deleted {instance_id}',
            headers=DEFAULT_HEADERS
        )
