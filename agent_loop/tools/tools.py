import json
import logging

from agent_loop.rich_console import RichConsole
from agent_loop.tools.create_todos import create_todos_json
from agent_loop.tools.mark_complete import mark_complete_json

logger = logging.getLogger(__name__)


class Tools:
    def __init__(self, rich_console: RichConsole):
        self.rich_console = rich_console
        self.todos: list[str] = []
        self.completed: list[bool] = []

    @property
    def tool_definition(self) -> list[dict[str, str]]:
        tools = [
            {"type": "function", "function": create_todos_json},
            {"type": "function", "function": mark_complete_json},
        ]
        logger.debug("Tool definition: %s", tools)
        return tools

    def get_todo_report(self) -> str:
        result = ""
        for index, todo in enumerate(self.todos):
            if self.completed[index]:
                result += f"Todo #{index + 1}: [green][strike]{todo}[/strike][/green]\n"
            else:
                result += f"Todo #{index + 1}: {todo}\n"
        self.rich_console.show(result)
        return result

    def _create_todos(self, descriptions: list[str]) -> str:
        self.todos.extend(descriptions)
        self.completed.extend([False] * len(descriptions))
        return self.get_todo_report()

    def _mark_complete(self, index: int, completion_notes: str) -> str:
        if 1 <= index <= len(self.todos):
            self.completed[index - 1] = True
        else:
            return "No todo at this index."
        self.rich_console.show(completion_notes)
        return self.get_todo_report()

    def handle_tool_calls(self, tool_calls: list) -> list[dict[str, str]]:
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            logger.debug("Tool called: %s with args: %s", tool_name, arguments)

            if tool_name == "create_todos":
                result = self._create_todos(**arguments)
            elif tool_name == "mark_complete":
                result = self._mark_complete(**arguments)
            else:
                result = {"error": f"unknown tool: {tool_name}"}

            results.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id,
                }
            )
        return results
