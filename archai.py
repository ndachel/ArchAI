#!/usr/bin/env python3

import json
import subprocess
import requests
import os
import datetime

MODEL = "ArchAI"

def log_event(event_type, data):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event": event_type,
        "data": data,
    }

    with open("./logs/archai.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")

def execute_tool(tool):
    if not os.path.exists(tool["path"]):
        raise FileNotFoundError(tool["path"])

    result = subprocess.run(
        [tool["path"]],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout

def parse_tool_request(response):
    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        return None

    if (
        data.get("action") == "tool_call"
        and "tool" in data
    ):
        return data

    return None

def ask_archai(messages):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": MODEL,
            "stream": False,
            "messages": messages,
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["message"]["content"]

def run_tool(tool_name):
    tool = tool_registry.get(tool_name)

    if tool is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    return execute_tool(tool)

def main():
    user_prompt = input("> ")
    log_event(
        "user_request",
        {
            "prompt": user_prompt
        }
    )
    messages = [
        {
            "role": "system",
            "content": f"""
Available tools:
{json.dumps(tool_registry, indent=2)}


If you need a tool, respond ONLY with valid JSON.

Tool request format:

{{
  "action": "tool_call",
  "tool": "tool_name",
  "arguments": {{}}
}}

If no tool is needed, answer normally.

Do not invent system information.
"""
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    while True:
        response = ask_archai(messages)

        tool_request = parse_tool_request(response)

        if not tool_request:
            break

        log_event("tool_request",{"tool": tool_request["tool"],"arguments": tool_request.get("arguments", {})})

        result = run_tool(tool_request["tool"])

        log_event("tool_result",{"tool": tool_request["tool"],"result": result})

        messages.append({
            "role": "assistant",
            "content": response
        })

        messages.append({
            "role": "tool",
            "content": result
        })

    response = ask_archai(messages)
    log_event("model_response",{"response": response})

    print(response)


tool_registry = {
    "system_info": {
        "description": "Returns current OS, kernel, CPU, GPU",
        "path": "./tools/system_info.py"
    },
    "disk_usage": {
        "description": "Returns filesystem capacity and usage",
        "path": "./tools/disk_usage.py"
    },
    "lspci": {
        "description": "Returns PCI hardware devices",
        "path": "./tools/lspci.py"
    },
    "pacman_query": {
        "description": "Returns installed package information",
        "path": "./tools/pacman_query.py"
    }
}


if __name__ == "__main__":
    main()
