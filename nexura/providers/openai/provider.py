from nexura.providers.provider import Provider


class OpenAIProvider(Provider):
    """
        OpenAI provider
    """
    def __init__(enabled: bool = True):
        super().__init__("OpenAI", "https://api.openai.com", "API_KEY", enabled=enabled)
