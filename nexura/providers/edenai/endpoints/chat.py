from dataclasses import dataclass, asdict
import typing

import httpx
from nexura.providers.endpoint import Endpoint
from nexura.utils.dataclass_with_doc import DataclassWithDoc


@dataclass
class _ToolCall(DataclassWithDoc):
    id: str
    name: str
    arguments: str


@dataclass
class _Tool(DataclassWithDoc):
    name: str
    description: str
    # The tool's parameters are specified using a JSON Schema object. Detailed format documentation is available in the JSON Schema reference.\n\nMake sure to well describe each parameter for best results.\n\nExample for a weather tool:\n\n`{"type": "object","properties": {"location": {"type": "string""description": "The geographical location for which weather data is requested."},"unit": {"type": "string", "enum": ["Celsius", "Fahrenheit"]"description": "The unit of measurement for temperature."}},"required": ["location"]}`
    parameters: str


@dataclass
class _ToolResult(DataclassWithDoc):
    # the id of the tool_call used to generate result
    id: str
    # the result of your function
    result: str


@dataclass
class _PreviousHistory(DataclassWithDoc):
    role: str
    message: str
    tools: typing.Optional[typing.List[_Tool]] = None
    tool_calls: typing.Optional[typing.List[_ToolCall]] = None


@dataclass
class ChatRequest(DataclassWithDoc):
    # It can be one (ex: 'amazon' or 'google') or multiple provider(s) (ex: 'amazon,microsoft,google') that the data will be redirected to in order to get the processed results. Providers can also be invoked with specific models (ex: providers: 'amazon/model1, amazon/model2, google/model3')
    providers: str
    # Providers in this list will be used as fallback if the call to provider in providers parameter fails. To use this feature, you must input only one provider in the `providers` parameter. but you can put up to 5 fallbacks. They will be tried in the same order they are input, and it will stop to the first provider who doesn't fail. Doesn't work with async subfeatures.
    fallback_providers: typing.List[str]
    # Optional : When set to true (default), the response is an object of responses with providers names as keys :\n\n`{"google" : { "status": "success", ... }, }`\n\nWhen set to false the response structure is a list of response objects :\n\n`[{"status": "success", "provider": "google" ... }, ]`.
    response_as_dict: typing.Optional[bool] = True
    # Optional : When set to false (default) the structure of the extracted items is list of objects having different attributes :\n\n`{'items': [{"attribute_1": "x1","attribute_2": "y2"}, ... ]}`\n\nWhen it is set to true, the response contains an object with each attribute as a list :\n\n`{ "attribute_1": ["x1","x2", ...], "attribute_2": [y1, y2, ...]}`
    attributes_as_list: typing.Optional[bool] = False
    show_base_64: bool = True
    # Optional : Shows the original response of the provider.\n\nWhen set to true, a new attribute original_response will appear in the response object.
    show_original_response: typing.Optional[bool] = False
    # Start your conversation here...
    text: typing.Optional[str] = None
    # A system message that helps set the behavior of the assistant. For example, 'You are a helpful assistant'.
    chatbot_global_action: typing.Optional[str] = None
    # A list containing all the previous conversations between the user and the chatbot AI. Each item in the list should be a dictionary with two keys: 'role' and 'message'. The 'role' key specifies the role of the speaker and can have the values 'user' or 'assistant'. The 'message' key contains the text of the conversation from the respective role. For example: [{'role': 'user', 'message': 'Hello'}, {'role': 'assistant', 'message': 'Hi, how can I help you?'}, ...]. This format allows easy identification of the speaker's role and their corresponding message.
    previous_history: typing.Optional[typing.List[_PreviousHistory]] = None
    # Higher values mean the model will take more risks and value 0 (argmax sampling) works better for scenarios with a well-defined answer.
    temperature: int = 0
    # The maximum number of tokens to generate in the completion. The token count of your prompt plus max_tokens cannot exceed the model's context length.
    max_tokens: int = 1000
    tool_choice: typing.Literal["auto", "required", "none"] = "auto"
    # A list of tools the model may generate the right arguments for.
    available_tools: typing.Optional[typing.List[_Tool]] = None
    # List of results obtained from applying the tool_call arguments to your own tool.
    tool_results: typing.Optional[typing.List[_ToolResult]] = None


@dataclass
class _Message(DataclassWithDoc):
    role: str
    message: str


@dataclass
class ChatResponse(DataclassWithDoc):
    generated_test: str
    message: typing.List[_Message]
    cost: float


class ChatEndpoint(Endpoint):
    """
    The Chat API is a specialized programming interface designed to allow users to interact with natural language processing models like GPT-3, and GPT-4. These models can be used to generate human-like responses to various inputs and queries.
    """

    def __init__(self):
        super().__init__("Chat", "POST", "/v2/text/chat", "Chat", "https://docs.edenai.co/reference/text_chat_create", enabled=True, examples_identifier="edenai/examples/chat.json")

    async def handle_request(self, body: ChatRequest) -> ChatResponse:
        r = await httpx.post(
            f"{self.provider.base_url}{self.path}",
            headers=self.provider.headers(),
            json=asdict(body),
        )

        return r  # type: ignore