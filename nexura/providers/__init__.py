import typing
from nexura.providers.provider import Provider
from nexura.providers.openai import openai_provider


class NexuraProvider:
    def __init__(self):
        self.providers: typing.List[Provider] = []

    def __generate_unique_provider_id(self, provider_name: str) -> str:
        provider_id = provider_name.lower().replace(" ", "-")
        i = 0
        while provider_id in [p.id for p in self.providers]:
            provider_id = f"{provider_id}-{i}"
            i += 1

        return provider_id

    def add_provider(
        self, provider: Provider
    ):
        provider_id = self.__generate_unique_provider_id(provider.name)
        provider.id = provider_id

        self.providers.append(provider)

    def get_provider(self, provider_id: str) -> Provider:
        for provider in self.providers:
            if provider.id == provider_id:
                return provider

        raise ValueError(f"Provider {provider_id} not found")

    async def handle_request(self, provider_id: str, endpoint_path: str, **kwargs):
        provider = self.get_provider(provider_id)
        endpoint = provider.get_endpoint(endpoint_path)
        return await endpoint.handle_request(**kwargs)


nexura_provider = NexuraProvider()


def initialize_providers():
    providers = [
        openai_provider,
    ]

    for provider in providers:
        nexura_provider.add_provider(provider)


initialize_providers()