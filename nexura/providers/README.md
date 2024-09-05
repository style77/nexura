# Providers

Abstract classes that define interfaces for the different types of providers that Nexura supports.

## List of Providers

- [OpenAI](https://openai.com)
- [EdenAI](https://edenai.co)

## How to Implement a Provider

To implement a new provider, you need to create a new directory in the `nexura/providers` directory (here) with the name of the provider. Inside this directory, you need to create a new Python file with the name `__init__.py` and `provider.py` (or any other name you prefer). The `provider.py` file should contain the abstract class that defines the interface for the provider. The `__init__.py` file should import the abstract class from the `provider.py` file and include the endpoints that the provider supports.

Here is an example of how the directory structure should look like:

```
nexura/providers/
    example/
        __init__.py
        provider.py
```

`provider.py` file:

```python
from nexura.providers.base import Provider


class ExampleProvider(Provider):
    """
        Example provider
    """
    def __init__(enabled: bool = True):
        super().__init__("Example", "https://api.example.com", os.getenv("EXAMPLE_PROVIDER_API_KEY"), enabled=enabled)

```

`__init__.py` file:

```python
from nexura.providers.example.endpoints.completions import ExampleEndpoint
from nexura.providers.example.provider import ExampleProvider


endpoints = [
    ExampleEndpoint()
]

example_provider = ExampleProvider()


def initialize_endpoints():
    for endpoint in endpoints:
        example_provider.add_endpoint(endpoint)


initialize_endpoints()
```

As you can see in the example above, the `provider.py` file contains the abstract class `ExampleProvider` that extends the `Provider` class. The `__init__.py` file imports the `ExampleProvider` class and initializes the provider with the endpoints that it supports, which are defined in the `endpoints` list.

### How to implement endpoint

To implement an endpoint, you need to create a new Python file in the provider directory with the name of the endpoint. The endpoint should be a class that extends the `Endpoint` class and implements the `handle_request` method. The `execute` method should make a request to the provider's API and return the response. You also need to create a dataclasses for the request and response objects documentation.

Here is an example of how the directory structure should look like:

```
nexura/providers/
    example/
        endpoints/
            __init__.py # empty file, to make the directory a package
            example.py
        __init__.py
        provider.py
```

`example.py` file:

```python
from dataclasses import dataclass, asdict
import typing

import httpx
from nexura.providers.endpoint import Endpoint
from nexura.utils.dataclass_with_doc import DataclassWithDoc

@dataclass
class _Message(DataclassWithDoc):  # We prefer to use underscore for nested dataclasses, to avoid conflicts with the main dataclass
    # We use above comments to document the dataclass fields, so the documentation is generated automatically
    role: str
    message: str  # but you are not forced to use them (we would be greatful if you do it, though)


@dataclass
class Request(DataclassWithDoc):
    message: typing.Optional[_Message] = None  # You can use nested dataclasses like this


@dataclass
class Response(DataclassWithDoc):
    response: str


class ExampleEndpoint(Endpoint):
    """
    Example endpoint
    """

    def __init__(self):
        super().__init__(name="Example", method="POST", path="/example", category="Example", original_docs_url="https://docs.example.com/", enabled=True)

    async def handle_request(self, body: Request) -> Response:
        r = await httpx.post(
            f"{self.provider.base_url}{self.path}",
            headers=self.provider.headers(),
            json=asdict(body),
        )

        return r  # type: ignore
```

> Documentation is core to the project, so we use comments to document the dataclasses fields. We use the `DataclassWithDoc` class to make the documentation generation easier.

### How to add the provider to the Nexura app

Lastly, you need to open the provider to app. To do this, you need to import the provider in the `nexura/providers/__init__.py` file and add it to the `providers` list in `initialize_providers` function.

`nexura/providers/__init__.py` file:
```python
...

nexura_provider = NexuraProvider()


def initialize_providers():
    providers = [
        openai_provider,
        edenai_provider,
        example_provider  # Add the provider here
    ]

    for provider in providers:
        nexura_provider.add_provider(provider)


initialize_providers()
```

### Add endpoint request and response example

To add an example of the request and response for the endpoint, you need to create a new Python file in the `nexura/providers/{provider}/examples` directory with the name `{endpoint}.json`. The file should contain the example request and response in following JSON format.

Here is an example of how the directory structure should look like:

```
nexura/providers/
    example/
        endpoints/
            __init__.py
            example.py
        examples/
            example.json
        __init__.py
        provider.py
```

`example.json` file:

```json
[
    {
        "label": "Example 1",
        "code": {
            "python": "print('Hello world')",
            "javascript": "console.log('Hello world')",
            "bash": "echo 'Hello world'"  // You can add more languages if needed
        },
        "response": {
            "type": "json",  // You can use 'json' or 'text' for the response type
            "content": "{
                \"response\": \"Hello world\"
            }"
        }
    },
    {  // You can also show more examples
        "label": "Example 2",
        "code": {
            "javascript": "console.log('Goodbye')",
        },
        "response": {
            "type": "text",
            "content": "Example code for making a POST request using cURL."
        }
    }
]
```