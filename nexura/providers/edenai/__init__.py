from nexura.providers.edenai.endpoints.chat import ChatEndpoint
from nexura.providers.edenai.provider import EdenAIProvider


endpoints = [
    ChatEndpoint()
]

edenai_provider = EdenAIProvider()


def initialize_endpoints():
    for endpoint in endpoints:
        edenai_provider.add_endpoint(endpoint)


initialize_endpoints()
