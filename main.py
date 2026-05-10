import ollama
ollama.pull("qwen3.5:2b")

import subprocess
import os

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes or overwrites a file with new content",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Executes a bash command and returns stdout+stderr",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command to execute"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_file",
            "description": "Executes a Python file and returns stdout+stderr",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the Python file to execute"}
                },
                "required": ["path"]
            }
        }
    },
]


def write_file(path: str, content: str) -> str:
    path = os.path.expanduser(path)
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"File {path} written successfully."
    except FileNotFoundError:
        return f"Error: directory does not exist for path '{path}'."

def read_file(path: str) -> str:
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: file '{path}' not found."

def run_command(command: str) -> str:
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=600
    )
    return result.stdout + result.stderr

def run_file(path: str) -> str:
    path = os.path.expanduser(path)
    try:
        result = subprocess.run(
            ["uv", "run", path], capture_output=True, text=True, timeout=600
        )
        return result.stdout + result.stderr
    except FileNotFoundError:
        return f"Error: file '{path}' not found."

available_tools = {
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
    "run_file": run_file,
}

import json

# USE PROGRAM.MD AS SYSTEM_PROMPT FOR THE AGENT
SYSTEM_PROMPT = open("/app/program.md").read()

def run_agent():
    messages = [
        {"role": "user", "content": "Read program.md and start the experiment setup."}
    ]

    while True:
        response = ollama.chat(
            model="qwen3.5:2b",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            tools=tools,
            think=False,
            options={
                "temperature": 1.0,
                "top_p": 1.0,
                "top_k": 20,
                "min_p": 0.0,
                "presence_penalty": 2.0,
                "repeat_penalty": 1.0,
                "num_ctx": 8192,
            }
        )

        message = response["message"]
        messages.append(message)

        if not message.get("tool_calls"):
            print("\n[AGENT]:", message["content"])
            messages.append({
                "role": "user",
                "content": "Do not explain code. Use your tools to take action. What is the next tool call you need to make?"
            })
            continue

        for tool_call in message["tool_calls"]:
            name = tool_call["function"]["name"]
            args = tool_call["function"]["arguments"]
            if isinstance(args, str):
                args = json.loads(args)

            print(f"\n[TOOL] {name}({args})")
            result = available_tools[name](**args)
            print(f"[RESULT] {result[:2000]}")

            messages.append({
                "role": "tool",
                "content": result,
            })

run_agent()