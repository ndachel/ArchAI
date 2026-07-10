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
