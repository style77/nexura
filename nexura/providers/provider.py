from typing import Dict, Self

from nexura.providers.endpoint import Endpoint


class Provider():
    def __init__(
        self,
        name: str,
        base_url: str,
        api_key: str,
        auth_schema: str = "Bearer",
        *,
        enabled: bool = True,
    ):
        self.id = None
        self.name = name
        self.base_url = base_url
        self.api_key = api_key
        self.auth_schema = auth_schema
        self.endpoints: Dict[str, "Endpoint"] = {}

        self.enabled = enabled

    def __generate_unique_endpoint_id(self, provider: Self, endpoint_name: str) -> str:
        endpoint_id = endpoint_name.lower().replace(" ", "-")
        i = 0
        while endpoint_id in [e.name for e in provider.endpoints]:
            endpoint_id = f"{endpoint_id}-{i}"
            i += 1

        return endpoint_id

    def headers(self, content_type: str = "application/json") -> Dict[str, str]:
        return {
            "Authorization": f"{self.auth_schema} {self.api_key}",
            "Content-Type": content_type,
        }

    def add_endpoint(self, endpoint: "Endpoint"):
        endpoint_id = self.__generate_unique_endpoint_id(self, endpoint.name)
        endpoint.id = endpoint_id
        endpoint.provider = self

        self.endpoints[endpoint.path] = endpoint

    def get_endpoint(self, endpoint_path: str) -> "Endpoint":
        return self.endpoints[endpoint_path]
