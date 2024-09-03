from nexura.providers.openai.endpoints.completions import ChatCompletionsEndpoint
from nexura.providers.openai.provider import OpenAIProvider


endpoints = [
    ChatCompletionsEndpoint()
]

openai_provider = OpenAIProvider()


def initialize_endpoints():
    for endpoint in endpoints:
        openai_provider.add_endpoint(endpoint)


initialize_endpoints()
