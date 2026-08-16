# Multiagent System Examples

This repository contains example ADK-based multiagent setups and utilities used for teaching and experimentation.

Quick structure

- `adk_multiagent_systems/` — example agent configurations and apps
  - `workflow_agents/agent.py` — a movie-pitch writing workflow using Sequential/Loop/Parallel agents
  - `parent_and_subagents/agent.py` — parent agent with subagents for travel planning
- `adk_utils/` — small utility plugins

## Architecture & Workflow

![Movie Pitch Workflow Diagram](./docs/workflow-diagram.png)

![Workflow Event Execution](./docs/workflow-events.png)

![Screenwriter Collaboration](./docs/screenwriter-output.png)

![Box Office Researcher Analysis](./docs/box-office-analysis.png)

![System Architecture](./docs/system-architecture.png)

Getting started

1. Create a Python virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r adk_multiagent_systems/requirements.txt
```

2. Create a `.env` file (copy `.env.example`) and set `MODEL` to your model identifier.
3. Run an example agent directly:

```bash
# Run the workflow agents example
python adk_multiagent_systems/workflow_agents/agent.py

# Or run the parent/subagents example
python adk_multiagent_systems/parent_and_subagents/agent.py
```

Notes

- These examples reference the Google ADK (`google.adk`) and other platform-specific SDKs. Ensure the required SDKs are installed and authenticated.
- The repository includes a `.gitignore` preconfigured to ignore local caches and secrets (e.g., `.local/`, `.npm/`, `.env`, shell histories).
