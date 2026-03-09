import logging

from agent_loop.client.openai import OpenAIClient
from agent_loop.parameters import AgentLoopSettings
from agent_loop.prompt import PromptBuilder
from agent_loop.rich_console import RichConsole
from agent_loop.tools.tools import Tools

logger = logging.getLogger(__name__)


class AgentLoop:
    def __init__(
        self,
        *,
        settings: AgentLoopSettings,
        prompt_builder: PromptBuilder,
        openai_client: OpenAIClient,
        tools: Tools,
        user_prompt: str,
    ):
        self.settings = settings
        self.prompt_builder = prompt_builder
        self.client = openai_client
        self.tools = tools
        self.user_prompt = user_prompt
        self.rich_console = RichConsole()

    def _loop(self, messages):
        done = False
        while not done:
            choice = self.client.create_chat_completion(
                model=self.settings.model,
                messages=messages,
                tools=self.tools.tool_definition,
                reasoning_effort="none",
            )
            if choice.finish_reason == "tool_calls":
                tool_calls = choice.message.tool_calls
                results = self.tools.handle_tool_calls(tool_calls)
                messages.append(choice.message)
                messages.extend(results)
            else:
                done = True
        self.rich_console.show(choice.message.content)

    def run(self):
        messages = [
            {"role": "system", "content": self.prompt_builder.system_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        self._loop(messages)
