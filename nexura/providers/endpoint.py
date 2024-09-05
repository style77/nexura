from abc import ABC, abstractmethod
import json
import os
import typing

from nexura.providers.example import Example


class Endpoint(ABC):
    def __init__(self, name: str, method: str, path: str, category: typing.Optional[str] = None, original_docs_url: typing.Optional[str] = None, *, enabled: bool = True, examples_identifier: typing.Optional[str] = None):
        self.id = None
        self.provider = None

        self.name = name
        self.method = method
        self.path = path
        self.category = category

        self.original_docs_url = original_docs_url
        self.enabled = enabled

        self.examples: typing.List[Example] = self.get_examples(examples_identifier) if examples_identifier else []

    def get_examples(self, examples_identifier: str):
        with open(f"{os.getcwd()}/nexura/providers/{examples_identifier}") as f:
            examples = json.load(f)

        return [Example(**example) for example in examples]

    @abstractmethod
    async def handle_request(self, **kwargs):
        raise NotImplementedError
