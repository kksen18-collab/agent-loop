import logging
from typing import TypeVar

from openai import NOT_GIVEN, OpenAI
from openai._types import NotGiven
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat.chat_completion import Choice
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def create_chat_completion(
        self,
        *,
        model: str,
        messages: list,
        tools: list[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        **kwargs,
    ) -> Choice:
        response = self.client.chat.completions.create(
            model=model, messages=messages, tools=tools, **kwargs
        )
        logger.debug("OpenAI response: %s", response)
        return response.choices[0]
