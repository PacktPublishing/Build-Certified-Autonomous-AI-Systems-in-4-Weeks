import ast
import json
import operator
from pathlib import Path
from typing import Any

from ollama import ResponseError, chat


# ---------------------------------------------------------
# Application configuration
# ---------------------------------------------------------

MODEL_NAME = "llama3.2:3b"
DATA_DIR = Path("data")
MAX_STEPS = 3

SYSTEM_PROMPT = """
You are a local multi-tool AI agent.

Your job:
- Understand the user's request
- Decide whether a tool is needed
- Return only valid JSON
- Never invent tool results
- If a tool result is available, use it to answer clearly

You have access to these tools:

1. calculator
   Use this for math.
   Arguments: {"expression": "2 + 2"}

2. file_reader
   Use this to read a specific local text file from the data folder.
   Arguments: {"filename": "ai_agents.txt"}

3. notes_search
   Use this to search all local notes in the data folder.
   Arguments: {"query": "agent loop"}

Return one of these JSON shapes:

If you need a tool:
{
  "action": "tool",
  "tool": "calculator | file_reader | notes_search",
  "args": {
    "expression": "...",
    "filename": "...",
    "query": "..."
  }
}

If you can answer now:
{
  "action": "final",
  "answer": "..."
}

Rules:
- Return JSON only
- Do not include markdown
- Do not include explanations outside JSON
- Use tools when the user asks for math, file content, or local notes
""".strip()


# ---------------------------------------------------------
# Safe calculator tool
# ---------------------------------------------------------

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate_math_node(node: ast.AST) -> float:
    """
    Safely evaluate a math expression AST node.
    """

    if isinstance(node, ast.Expression):
        return evaluate_math_node(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
        left = evaluate_math_node(node.left)
        right = evaluate_math_node(node.right)
        return ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_UNARY_OPERATORS:
        operand = evaluate_math_node(node.operand)
        return ALLOWED_UNARY_OPERATORS[type(node.op)](operand)

    raise ValueError("Unsupported or unsafe math expression.")


def calculator(expression: str) -> str:
    """
    Calculate a safe math expression.
    """

    try:
        parsed = ast.parse(expression, mode="eval")
        result = evaluate_math_node(parsed)
        return f"Calculation result: {expression} = {result}"

    except Exception as error:
        return f"Calculator error: {error}"


# ---------------------------------------------------------
# File reader tool
# ---------------------------------------------------------


def file_reader(filename: str) -> str:
    """
    Read a text file from the data folder.
    """

    safe_name = Path(filename).name
    file_path = DATA_DIR / safe_name

    if not file_path.exists():
        return f"File not found: {safe_name}"

    if file_path.suffix.lower() != ".txt":
        return "Only .txt files are allowed in this beginner lab."

    try:
        content = file_path.read_text(encoding="utf-8")
        return f"Content of {safe_name}:\n{content}"

    except OSError as error:
        return f"File reader error: {error}"


# ---------------------------------------------------------
# Notes search tool
# ---------------------------------------------------------


def notes_search(query: str) -> str:
    """
    Search all .txt files in the data folder for matching lines.
    """

    if not DATA_DIR.exists():
        return "The data folder does not exist."

    query_words = query.lower().split()
    matches: list[str] = []

    for file_path in DATA_DIR.glob("*.txt"):
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue

        for line_number, line in enumerate(lines, start=1):
            lower_line = line.lower()

            if any(word in lower_line for word in query_words):
                matches.append(
                    f"{file_path.name}, line {line_number}: {line}"
                )

    if not matches:
        return f"No notes found for query: {query}"

    return "Search results:\n" + "\n".join(matches[:8])


# ---------------------------------------------------------
# Tool registry
# ---------------------------------------------------------

TOOLS = {
    "calculator": calculator,
    "file_reader": file_reader,
    "notes_search": notes_search,
}


# ---------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------


def extract_json(text: str) -> dict[str, Any]:
    """
    Parse JSON from the model response.
    """

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("Model did not return JSON.")

    return json.loads(text[start : end + 1])



def ask_llm_for_next_action(user_request: str, observations: list[str]) -> dict[str, Any]:
    """
    Ask Ollama whether the agent should use a tool or return a final answer.
    """

    observation_text = "\n\n".join(observations) if observations else "No tool observations yet."

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
User request:
{user_request}

Tool observations so far:
{observation_text}

Decide the next step.
Return only valid JSON.
""".strip(),
        },
    ]

    response = chat(
        model=MODEL_NAME,
        messages=messages,
        format="json",
    )

    return extract_json(response.message.content)



def run_tool(tool_name: str, args: dict[str, Any]) -> str:
    """
    Validate and run the selected tool.
    """

    if tool_name not in TOOLS:
        return f"Tool error: Unknown tool '{tool_name}'."

    if not isinstance(args, dict):
        return "Tool error: Tool arguments must be a dictionary."

    if tool_name == "calculator":
        expression = str(args.get("expression", "")).strip()
        if not expression:
            return "Tool error: calculator requires an expression."
        return calculator(expression)

    if tool_name == "file_reader":
        filename = str(args.get("filename", "")).strip()
        if not filename:
            return "Tool error: file_reader requires a filename."
        return file_reader(filename)

    if tool_name == "notes_search":
        query = str(args.get("query", "")).strip()
        if not query:
            return "Tool error: notes_search requires a query."
        return notes_search(query)

    return "Tool error: Tool could not be executed."


# ---------------------------------------------------------
# Agent loop
# ---------------------------------------------------------


def run_agent(user_request: str) -> str:
    """
    Run a small ReAct-style agent loop.
    """

    observations: list[str] = []

    for step in range(1, MAX_STEPS + 1):
        print(f"\nAgent step {step}...")

        decision = ask_llm_for_next_action(user_request, observations)
        action = decision.get("action")

        if action == "final":
            return str(decision.get("answer", "I do not have a final answer."))

        if action == "tool":
            tool_name = str(decision.get("tool", "")).strip()
            args = decision.get("args", {})

            print(f"Tool selected: {tool_name}")
            print(f"Tool args: {args}")

            observation = run_tool(tool_name, args)
            print(f"Observation: {observation}")

            observations.append(observation)
            continue

        return "Agent error: The model returned an unknown action."

    return (
        "I reached the maximum number of tool steps. "
        "Here is what I found:\n" + "\n".join(observations)
    )


# ---------------------------------------------------------
# Terminal UI
# ---------------------------------------------------------


def display_welcome_message() -> None:
    print("=" * 64)
    print("MULTI-TOOL AI AGENT WITH OLLAMA")
    print(f"Local model: {MODEL_NAME}")
    print("=" * 64)
    print("Commands:")
    print("  /help   Show example prompts")
    print("  /exit   Close the application")
    print()



def display_help() -> None:
    print("\nTry these prompts:\n")
    print("1. What is 25 * 18 + 40?")
    print("2. Search my notes for agent loop.")
    print("3. Read the file ai_agents.txt and summarize it.")
    print("4. What does week 3 focus on in my bootcamp plan?")
    print()



def main() -> None:
    display_welcome_message()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "/exit":
            print("Goodbye!")
            break

        if user_input.lower() == "/help":
            display_help()
            continue

        try:
            answer = run_agent(user_input)
            print(f"\nAssistant: {answer}\n")

        except ConnectionError:
            print("\nCould not connect to Ollama. Make sure Ollama is running.\n")

        except ResponseError as error:
            print(f"\nOllama error: {error}\n")
            print(f"If the model is missing, run: ollama pull {MODEL_NAME}\n")

        except Exception as error:
            print(f"\nUnexpected error: {error}\n")


if __name__ == "__main__":
    main()
