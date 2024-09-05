import typing
from nexura.models.response import Response
from nexura.providers import nexura_provider


async def handle_request(provider: str, endpoint_id: str, body: typing.Any) -> Response:
    response = nexura_provider.handle_request(provider, endpoint_id, body=body)

    return response
