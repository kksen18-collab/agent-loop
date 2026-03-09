from agent_loop.client.openai import OpenAIClient
from agent_loop.logger import setup_logging
from agent_loop.loop import AgentLoop
from agent_loop.parameters import AgentLoopSettings
from agent_loop.prompt import PromptBuilder
from agent_loop.rich_console import RichConsole
from agent_loop.tools.tools import Tools


def main():
    setup_logging()
    try:
        user_prompt = input("What would you like to do?\n")
    except KeyboardInterrupt:
        print("\nGoodbye!")
        return
    settings = AgentLoopSettings()  # type: ignore
    openai_client = OpenAIClient(api_key=settings.openai_api_key)
    rich_console = RichConsole()
    tools = Tools(rich_console=rich_console)
    prompt_builder = PromptBuilder()
    agent_loop = AgentLoop(
        settings=settings,
        openai_client=openai_client,
        prompt_builder=prompt_builder,
        tools=tools,
        user_prompt=user_prompt,
    )
    agent_loop.run()


if __name__ == "__main__":
    main()
