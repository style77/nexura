import os
from nexura.providers.base import Provider


class EdenAIProvider(Provider):
    """
        EdenAI provider
    """
    def __init__(enabled: bool = True):
        super().__init__("EdenAI", "https://api.edenai.run", os.getenv("EDENAI_API_KEY"), enabled=enabled)
