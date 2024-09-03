from dataclasses import asdict, dataclass
import typing

import httpx
from nexura.providers.endpoint import Endpoint
from nexura.utils.dataclass_with_doc import DataclassWithDoc


@dataclass
class _SystemMessage(DataclassWithDoc):
    # The contents of the system message.
    content: str
    # The role of the messages author, in this case system.
    role: typing.Literal["system"] = "system"
    # An optional name for the participant. Provides the model information to differentiate between participants of the same role.
    name: typing.Optional[str] = None


@dataclass
class _UserMessage(DataclassWithDoc):
    # The contents of the user message.
    content: str
    # The role of the messages author, in this case user.
    role: typing.Literal["user"] = "user"
    # An optional name for the participant. Provides the model information to differentiate between participants of the same role.
    name: typing.Optional[str] = None


@dataclass
class _Function(DataclassWithDoc):
    # The name of the function to call.
    name: str
    # The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function.
    arguments: str


@dataclass
class _ToolCall(DataclassWithDoc):
    # The ID of the tool call.
    id: str
    # The type of the tool. Currently, only function is supported.
    type: str
    # The function that the model called.
    function: _Function


@dataclass
class _AssistantMessage(DataclassWithDoc):
    # The contents of the assistant message. Required unless tool_calls or function_call is specified.
    content: typing.Optional[str] = None
    # The refusal message by the assistant.
    refusal: typing.Optional[str] = None
    # The role of the messages author, in this case assistant.
    role: typing.Literal["assistant"] = "assistant"
    # An optional name for the participant. Provides the model information to differentiate between participants of the same role.
    name: typing.Optional[str] = None
    # The tool calls generated by the model, such as function calls.
    tool_calls: typing.Optional[typing.List[_ToolCall]] = None


@dataclass
class CompletionsRequest(DataclassWithDoc):
    # A list of messages comprising the conversation so far.
    messages: typing.List[typing.Union[_SystemMessage, _UserMessage, _AssistantMessage]]
    # ID of the model to use.
    model: typing.Literal["gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"]
    # Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
    frequency_penalty: typing.Optional[float] = 0
    # Modify the likelihood of specified tokens appearing in the completion.\nAccepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.
    logit_bias: typing.Optional[typing.Dict[str, int]] = None
    # Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the `content` of `message`.
    logprobs: typing.Optional[bool] = False
    # An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. `logprobs` must be set to `true` if this parameter is used.
    top_logprobs: typing.Optional[int] = None
    # The maximum number of [tokens](https://platform.openai.com/tokenizer) that can be generated in the chat completion. The total length of input tokens and generated tokens is limited by the model's context length. [Example Python code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken) for counting tokens.
    max_tokens: typing.Optional[int] = None
    # How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep `n` as `1` to minimize costs.
    n: typing.Optional[int] = 1
    # Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
    presence_penalty: typing.Optional[float] = 0
    # [DISABLED:"response_format TODO https://platform.openai.com/docs/api-reference/chat/create#chat-create-response_format"]
    response_format: typing.Optional[typing.Any] = None
    # [BETA] This feature is in Beta. If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed, and you should refer to the system_fingerprint response parameter to monitor changes in the backend.
    seed: typing.Optional[int] = None
    # Specifies the latency tier to use for processing the request. This parameter is relevant for customers subscribed to the scale tier service:\n\n- If set to 'auto', the system will utilize scale tier credits until they are exhausted.\n- If set to 'default', the request will be processed using the default service tier with a lower uptime SLA and no latency guarentee.\n- When not set, the default behavior is 'auto'.\nWhen this parameter is set, the response body will include the service_tier utilized.
    service_tier: typing.Optional[typing.Literal["auto", "default"]] = None
    # Up to 4 sequences where the API will stop generating further tokens.
    stop: typing.Optional[typing.Union[str, typing.List[str]]] = None
    # [DISABLED:"stream TODO https://platform.openai.com/docs/api-reference/chat/create#chat-create-stream"] If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format) as they become available, with the stream terminated by a `data: [DONE]` message. [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).
    stream: typing.Optional[bool] = False


@dataclass
class _Usage(DataclassWithDoc):
    # Number of tokens in the generated completion.
    completion_tokens: int
    # Number of tokens in the prompt.
    prompt_tokens: int
    # Total number of tokens used in the request (prompt + completion).
    total_tokens: int


@dataclass
class _Message(DataclassWithDoc):
    # The contents of the message.
    content: str
    # The role of the author of this message.
    role: str
    # The refusal message generated by the model.
    refusal: typing.Optional[str] = None
    # The tool calls generated by the model, such as function calls.
    tool_calls: typing.Optional[typing.List[_ToolCall]] = None


@dataclass
class _Choice(DataclassWithDoc):
    # The reason the model stopped generating tokens. This will be `stop` if the model hit a natural stop point or a provided stop sequence, `length` if the maximum number of tokens specified in the request was reached, `content_filter` if content was omitted due to a flag from our content filters, `tool_calls` if the model called a tool, or `function_call` (deprecated) if the model called a function.
    finish_reason: typing.Literal[
        "stop", "length", "content_filter", "tool_calls", "function_call"
    ]
    # The index of the choice in the list of choices.
    index: int
    # A chat completion message generated by the model.
    message: _Message
    # Log probability information for the choice.
    logprobs: typing.Optional[typing.Dict[str, typing.Any]] = None


@dataclass
class CompletionResponse(DataclassWithDoc):
    # A unique identifier for the chat completion.
    id: str
    # A list of chat completion choices. Can be more than one if n is greater than 1.
    choices: typing.List[_Choice]
    # The Unix timestamp (in seconds) of when the chat completion was created.
    created: int
    # The model used for the chat completion.
    model: str
    # The object type, which is always `chat.completion`.
    object: str
    # Usage statistics for the completion request.
    usage: _Usage
    # The service tier used for processing the request. This field is only included if the service_tier parameter is specified in the request.
    service_tier: typing.Optional[typing.Literal["auto", "default"]] = None
    # This fingerprint represents the backend configuration that the model runs with.\n\nCan be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism.
    system_fingerprint: typing.Optional[str] = None


class ChatCompletionsEndpoint(Endpoint):
    """
    Given a list of messages comprising a conversation, the model will return a response.
    """

    def __init__(self):
        super().__init__("Chat Completions", "POST", "/v1/chat/completions", "Chat", "https://platform.openai.com/docs/api-reference/chat/create", enabled=True)

    async def handle_request(self, body: CompletionsRequest) -> CompletionResponse:
        r = await httpx.post(
            f"{self.provider.base_url}{self.path}",
            headers=self.provider.headers(),
            json=asdict(body),
        )

        return r  # type: ignore
