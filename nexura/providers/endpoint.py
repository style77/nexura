from abc import ABC, abstractmethod
import typing


class Endpoint(ABC):
    def __init__(self, name: str, method: str, path: str, category: typing.Optional[str] = None, original_docs_url: typing.Optional[str] = None, *, enabled: bool = True):
        self.id = None
        self.provider = None

        self.name = name
        self.method = method
        self.path = path
        self.category = category

        self.original_docs_url = original_docs_url
        self.enabled = enabled

    @abstractmethod
    async def handle_request(self, **kwargs):
        raise NotImplementedError
