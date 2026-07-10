# ArchAI 

This is a test. Please don't use this for real work, but feel free to improve!

A local, opinionated AI assistant built around Ollama, designed to provide a grounded interface to a Linux system through controlled capabilities.

ArchAI is an experiment in building an "AI shell" where the language model provides reasoning and intent interpretation, while a controller layer manages access to deterministic system tools.

The goal is not simply a chatbot running locally. The goal is a capability-based assistant where:

- the model reasons,
- tools provide facts,
- the controller enforces boundaries.

---

## Design Philosophy

Large language models are excellent at interpretation and reasoning, but they are not authoritative sources of truth about the environment they run in.

ArchAI separates:

             User Intent
                 |
                 v
            ArchAI Model
                 |
          Structured Intent
                 |
                 v
         Capability Controller
                 |
      +----------+----------+
      |          |          |
      v          v          v
system_info  disk_usage  other tools...etc 
      |
      v
 Ground Truth


The model does not directly execute commands.

The controller decides which capabilities exist and executes only registered tools.

---

---

## Components

### Ollama

Runs the local language model.

Responsibilities:

- language understanding
- reasoning
- intent interpretation
- generating structured tool requests

Ollama does not directly access the host system.

---

### ArchAI Controller (`archai.py`)

The controller is the bridge between the model and system capabilities.

Responsibilities:

- sends prompts to Ollama
- provides available tool descriptions
- parses structured tool requests
- validates requested capabilities
- executes approved tools
- returns tool results to the model
- logs interactions

---

### Modelfile

Defines ArchAI's personality and behavioral constraints.

Examples:

- prefer accuracy over agreement
- avoid inventing facts
- be cautious with assumptions

The Modelfile defines **behavior**, not capabilities.

---

## Tool System

Tools are external executable capabilities.

Example registry entry:

```json
{
  "name": "system_info",
  "description": "Returns current OS, kernel, CPU, GPU",
  "path": "./tools/system_info/system_info.py"
}
```
A tool:

 - receives no implicit model authority
 - returns structured information
 - can be independently tested
 - can be added without rebuilding the model

### Current Tools
#### system_info

Returns:

operating system
kernel
architecture
CPU
GPU

Example:

{
  "os": "CachyOS",
  "kernel": "7.1.2-3-cachyos",
  "architecture": "x86_64",
  "cpu": "13th Gen Intel(R) Core(TM) i7-13700K",
  "gpu": "NVIDIA GeForce RTX 4090"
}
#### disk_usage

Returns filesystem capacity information.

#### lspci

Returns PCI hardware inventory.

Useful for hardware discovery.

#### pacman_query

Returns installed package inventory.

Currently informational only.

### Tool Invocation Protocol

ArchAI requests tools using structured JSON:
```json
{
  "action": "tool_call",
  "tool": "system_info",
  "arguments": {}
}
```

The controller:

 - Parses the request.
 - Verifies the tool exists.
 - Executes the registered capability.
 - Returns results to the model.
 - Does some logging

ArchAI records interactions in JSON Lines format:

logs/archai.jsonl

Logged events include:

 - user requests
 - model responses
 - tool requests
 - tool results

-----

Start Ollama:

docker compose up -d

Run ArchAI:

./archai.py

Example:

> What GPU do I have?

ArchAI:
You have an NVIDIA GeForce RTX 4090.

---
This is an early prototype.

Future Directions

Potential next steps:

Multi-step planning

Allow:

Question
   |
system_info
   |
disk_usage
   |
hardware analysis
   |
answer
Capability permissions

Introduce policy controls:

{
  "name": "package_install",
  "risk": "high",
  "requires_confirmation": true
}
Evaluator / Supervisor Layer

Add a supervisory model or rules engine to evaluate:

whether the requested action is appropriate
whether the tool is authorized
whether the answer is grounded
AI Shell Interface

Long-term concept:

Intent
  |
AI reasoning
  |
Capability broker
  |
Linux system

A natural language interface to a system where the AI has useful capabilities without unrestricted authority.

Status

Prototype phase.

The current milestone demonstrates:

local inference
grounded system awareness
capability-based tools
structured tool invocation
auditable execution
