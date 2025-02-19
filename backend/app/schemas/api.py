from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
import re
from app.schemas.models import Book, Message
from openapi_pydantic.v3 import OpenAPI, Info, PathItem, Operation
from openapi_pydantic.util import PydanticSchema, construct_open_api_with_schema_class

from typing import Dict, Any
import yaml


class BookRequest(BaseModel):
    query: str = Field(
        ..., title="Search Query", description="The query string for book search"
    )


class BookResponse(BaseModel):
    recommendations: List[Book] = Field(
        ...,
        title="Recommended Books",
        description="List of recommended books based on search query",
    )
    message: str = Field(
        ...,
        title="Message",
        description="A generated explanation of why the recommended books are relevant to the query",
    )


class CompletionRequest(BaseModel):
    """
    Represents a chat request for the language model (LLM).

    Attributes:
      - model: The identifier for the LLM to use.
      - temperature: A float value that controls the randomness of the LLM output.
      - messages: A list of chat messages that form the conversation history.
      - max_tokens: The maximum number of tokens that the model can generate.
      - response_format: Specifies the format of the model's output (e.g., 'json_object').
      - stream: If set to True, the response will be sent as partial message deltas via SSE.
    """

    model: str = Field(
        "deepseek-chat",
        title="Model Identifier",
        description="The identifier for the language model (e.g., 'deepseek-chat') that will process the conversation.",
        examples=["deepseek-chat", "deepseek-reasoner"],
    )
    temperature: Optional[float] = Field(
        1.3,
        title="Temperature Parameter",
        description=(
            "Controls the randomness of the generated response. Lower values yield more deterministic output, "
            "while higher values increase variability."
        ),
        examples=[0.5, 1.0, 1.3],
    )
    messages: List[Message] = Field(
        ...,
        title="Conversation History",
        description=(
            "A list of chat messages comprising the conversation history. "
            "The first message typically contains the user's initial query. Each message must include a role and its content."
        ),
        example=[
            {
                "role": "user",
                "content": "Please produce a JSON output that lists anime similar to Hunter x Hunter.",
            }
        ],
    )
    max_tokens: int = Field(
        1000,
        title="Max Tokens",
        description=(
            "The maximum number of tokens that the model is allowed to generate in response. "
            "Increasing this value may result in longer responses."
        ),
        example=1000,
    )
    response_format: str = Field(
        "json_object",
        title="Response Format",
        description=(
            "Specifies the format of the model's output. For example, setting this to 'json_object' instructs the model "
            "to produce output that is valid JSON. When using 'json_object', at least one user or system message must instruct "
            "the model to produce JSON output (e.g., by including 'json' in the message content)."
        ),
        examples=["text", "json_object"],
    )
    stream: bool = Field(
        False,
        title="Stream",
        description=(
            "If set to True, partial message deltas will be sent. Tokens will be delivered as data-only server-sent events (SSE) "
            "as they become available, with the stream terminated by a final 'data: [DONE]' message."
        ),
        example=True,
    )

    @model_validator(mode="before")
    def validate_json_output_instruction(cls, values):
        print("Validating the JSON output instruction")

        print("values")
        print(type(values))
        print(values)

        response_format = values.get("response_format")
        print(f"response_format: {response_format}")
        messages = values.get("messages", [])
        print("messages: ", messages)
        if response_format == "json_object":
            # Check that at least one user or system message instructs the model to produce JSON output.
            instruction_found = any(
                msg.role in ("user", "system")
                and re.search(r"\bjson\b", msg.content, re.IGNORECASE)
                for msg in messages
            )
            if not instruction_found:
                raise ValueError(
                    "When response_format is 'json_object', at least one user or system message must instruct "
                    "the model to produce JSON output (e.g., by including 'json' in the message content)."
                )
        return values

    class Config:
        json_schema_extra = {
            "example": {
                "model": "deepseek-chat",
                "temperature": 1.3,
                "messages": [
                    {
                        "role": "user",
                        "content": "Please produce a JSON output that lists anime similar to Hunter x Hunter.",
                    }
                ],
                "max_tokens": 1000,
                "response_format": "json_object",
                "stream": True,
            }
        }


class CompletionResponse(BaseModel):
    """
    Represents the final aggregated response from the language model (LLM) after streaming.

    **Streaming Response Details:**

    This endpoint returns a streaming response with a content type of `text/event-stream`.
    As tokens become available, partial message deltas are sent as individual SSE events. Each event is formatted as:

    ```
    data: <JSON chunk>\n\n
    ```

    For example, the streaming events may be:

    ```
    data: {"choices": [{"delta": {"content": "Hello", "role": "assistant"}, ...}]}
    data: {"choices": [{"delta": {"content": "!", "role": "assistant"}, ...}]}
    data: {"choices": [{"delta": {"content": " How", "role": "assistant"}, ...}]}
    data: {"choices": [{"delta": {"content": " can", "role": "assistant"}, ...}]}
    data: {"choices": [{"delta": {"content": " I", "role": "assistant"}, ...}]}
    data: {"choices": [{"delta": {"content": " assist", "role": "assistant"}, ...}]}
    data: {"choices": [{"delta": {"content": " you", "role": "assistant"}, ...}]}
    data: {"choices": [{"delta": {"content": " today", "role": "assistant"}, ...}]}
    data: {"choices": [{"delta": {"content": "?", "role": "assistant"}, ...}]}
    data: {"choices": [{"delta": {"content": "", "role": null}, "finish_reason": "stop", ...}]}
    data: [DONE]
    ```

    The client is expected to concatenate these chunks into a single aggregated output. The final aggregated response should then match the schema below, for example:

    ```json
    {
      "messages": [
         {
           "role": "assistant",
           "content": "Hello! How can I assist you today?"
         }
      ]
    }
    ```
    """

    messages: List[Message] = Field(
        ...,
        title="Response Messages",
        description=(
            "A list of messages returned by the language model, including the assistant's generated response. "
            "For streaming responses, the final aggregated output is expected to conform to this schema."
        ),
        example=[
            {"role": "assistant", "content": "Hello! How can I assist you today?"}
        ],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "assistant",
                        "content": "Hello! How can I assist you today?",
                    }
                ]
            }
        }


class Error(BaseModel):
    code: str
    message: str


def construct_base_open_api() -> OpenAPI:
    return OpenAPI(
        openapi="3.1.0",
        info=Info(
            title="Conversational Book Search API",
            version="0.0.1",
        ),
        servers=[
            {
                "url": "http://localhost:8000",
                "description": "Local Python server",
            },
            {
                "url": "https://api.example.com",
                "description": "Production server",
            },
        ],
        paths={
            "/api/chat/stream": PathItem(
                post=Operation(
                    operationId="streamLLM",
                    description="Chat with the language model (LLM) and receive streaming responses.",
                    responses={
                        "200": {
                            "content": {
                                "text/event-stream": {
                                    "schema": PydanticSchema(
                                        schema_class=CompletionResponse
                                    ),
                                }
                            },
                            "description": "OK, returns a streamed sequence of chat completion chunk objects",
                        }
                    },
                )
            )
        },
    )


open_api = construct_base_open_api()
open_api = construct_open_api_with_schema_class(open_api)

if __name__ == "__main__":
    with open("openapi.yaml", "w") as file:
        file.write(
            yaml.dump(
                open_api.model_dump(
                    by_alias=True,
                    mode="json",
                    exclude_none=True,
                    exclude_unset=True,
                ),
                sort_keys=False,
            )
        )
