# Agent Loop

A manual agentic loop implementation that uses standard OpenAI API calls to enable autonomous task planning and execution. This project demonstrates how to build an agent system without relying on OpenAI's Agent SDK.

## Overview

Agent Loop is a Python-based framework that allows an AI agent to:
1. Receive a user request
2. Create a plan of actionable to-do items
3. Execute each step sequentially
4. Track completion status
5. Provide a final response

The agent autonomously decides which tools to use and in what order to solve the given problem.

## Features

- **Manual Agentic Loop**: Implements a full agent loop using standard LLM function calls (not the OpenAI Agent SDK)
- **Tool-Based Problem Solving**: The LLM can create and mark to-do items to break down complex tasks
- **Rich Console Output**: Beautiful formatted output using Rich library
- **Fully Configurable**: Settings managed via environment variables
- **Logging Support**: Comprehensive logging for debugging and monitoring
- **Type-Safe**: Built with Pydantic for robust data validation

## Installation

### Prerequisites
- Python 3.13+
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd agent-loop
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
```

3. Install the package with dependencies:
```bash
pip install -e .
```

4. Create a `.env` file with your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-api-key-here
MODEL=gpt-4  # or your preferred model
```

## Usage

Run the agent with a user prompt:

```bash
python -m agent_loop.app
```

Then enter your request when prompted. Example:
```
What would you like to do?
What is the square root of 256?
```

The agent will:
1. Create a plan of steps
2. Execute each step
3. Display the result

## Project Structure

```
agent_loop/
├── app.py                 # Main entry point
├── loop.py               # Core AgentLoop class implementing the agentic loop
├── parameters.py         # Configuration settings using Pydantic
├── prompt.py             # System prompt builder
├── logger.py             # Logging configuration
├── rich_console.py       # Rich console output utilities
├── client/
│   └── openai.py         # OpenAI API client wrapper
└── tools/
    ├── tools.py          # Tool handler and manager
    ├── create_todos.py   # Create to-do items tool definition
    └── mark_complete.py  # Mark to-do complete tool definition
```

## How It Works

### The Agentic Loop

The core loop is implemented in [loop.py](loop.py) and operates as follows:

1. **Initialize**: System prompt and user request are sent to the LLM
2. **Loop**:
   - LLM receives the current conversation state
   - LLM decides to either:
     - Call a tool (create_todos or mark_complete)
     - Finish and provide the final answer
   - If tool is called:
     - Tool execution results are added to messages
     - Loop continues with the new context
   - If done (no tool call):
     - Loop terminates
     - Final response is displayed

### Available Tools

**create_todos**
- Creates a list of to-do items from descriptions
- Helps the agent break down problems into steps
- Parameters: `descriptions` (array of strings)

**mark_complete**
- Marks a to-do item as complete
- Provides completion notes
- Parameters: `index` (1-based), `completion_notes` (string)

## Implementation Details

### What Was Done

This project implements a **manual agentic loop** using standard OpenAI API calls instead of relying on OpenAI's higher-level Agent SDK. Key aspects:

- **Manual Message Management**: The loop explicitly manages conversation history and message passing
- **Tool Call Handling**: Parses and executes tool calls based on LLM responses
- **State Tracking**: Maintains to-do items and completion status throughout the conversation
- **Iterative Execution**: Continues the loop until the LLM signals completion (finish_reason != "tool_calls")

### Tools & Technologies Used

- **[OpenAI API](https://openai.com/api/)**: For LLM inference with function/tool calling capabilities
- **[Pydantic](https://docs.pydantic.dev/)**: Type validation and settings management
- **[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)**: Environment-based configuration
- **[Rich](https://rich.readthedocs.io/)**: Beautiful terminal output formatting
- **[Python Requests](https://requests.readthedocs.io/)**: HTTP client (dependency)
- **[python-dotenv](https://python-dotenv.readthedocs.io/)**: Environment variable loading
- **[Gradio](https://www.gradio.app/)**: Web interface capability (optional)

## Configuration

Settings are managed in [parameters.py](agent_loop/parameters.py):

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `MODEL`: The model to use (default: gpt-5.2)

All settings are loaded from the `.env` file and validated using Pydantic.

## Logging

Logging is configured in [logger.py](agent_loop/logger.py). Debug logs will show:
- Tool definitions
- Tool calls with arguments
- OpenAI API responses

## Example

```
What would you like to do?
> Calculate 15% tip on a $120 bill

Agent creates a plan:
  Todo #1: Calculate 15% of $120
  Todo #2: Add the tip to the original amount for total

Agent executes plan and returns:
  The tip on a $120 bill at 15% is $18.
  The total including tip is $138.
```

## License

This project is open source and available under the MIT License.
