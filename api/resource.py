from aiohttp.web import UrlDispatcher
from api.rest import InstanceEndpoint, ListEndpoint


class GenericResource:
    """
    Handles routing based upon given model
    :param resource_name: resource name used in routing
    :param model: model to organise resource around
    """

    def __init__(self, resource_name, model):
        self.resource_name = resource_name

        self.instance_endpoint = InstanceEndpoint(model)
        self.list_endpoint = ListEndpoint(model)

    def register(self, router: UrlDispatcher):
        router.add_route(
            '*', f'/{self.resource_name}/{{instance_id}}',
            self.instance_endpoint.dispatch
        )
        router.add_route(
            '*', f"/{self.resource_name}",
            self.list_endpoint.dispatch
        )
