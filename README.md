# Multiagent System Examples

This repository contains example ADK-based multiagent setups and utilities used for teaching and experimentation.

Quick structure

- `adk_multiagent_systems/` — example agent configurations and apps
  - `workflow_agents/agent.py` — a movie-pitch writing workflow using Sequential/Loop/Parallel agents
  - `parent_and_subagents/agent.py` — parent agent with subagents for travel planning
- `adk_utils/` — small utility plugins

## Architecture & Workflow

### Movie Pitch Workflow
This example demonstrates a complex multiagent workflow with Sequential, Loop, and Parallel agents working together to create a movie pitch:

![Movie Pitch Workflow Diagram](./docs/workflow-diagram.png)

The workflow includes:
- **SequentialAgent** (`film_concept_team`) - Establishes the core concept
- **LoopAgent** (`writers_room`) - Iteratively refines the screenplay with research and feedback loops
- **ParallelAgent** (`preproduction_team`) - Executes parallel research and planning tasks

### Workflow in Action
Example of the research step in execution:

![Workflow Event Execution](./docs/workflow-events.png)

### Creative Collaboration
The screenwriter agent produces detailed outputs:

![Screenwriter Collaboration](./docs/screenwriter-output.png)

### Box Office Analysis
Market research and commercial viability assessment:

![Box Office Researcher Analysis](./docs/box-office-analysis.png)

**Target Audiences:**
1. The "Prestige" & Adult Drama Crowd (Ages 35+): Highly loyal to theaters for well-reviewed, intellectual dramas. They drove the success of *Oppenheimer*, *The King's Speech*, and *One Life*.
2. Women in STEM / Feminist Cinema Enthusiasts: The narrative of a brilliant woman fighting institutional sexism in the 1940s is incredibly timely. This group will champion the film on social media.
3. Classic Hollywood / Cinephile Demographic: Film buffs will be drawn to the behind-the-scenes depiction of MGM, Louis B. Mayer, Howard Hughes, and the Golden Age studio system.
4. Tech-History Enthusiasts: The unique mechanical integration of player pianos and radio technology appeals to audiences who love historical innovation and "how-it-was-made" stories.

**Commercial Strengths & Market Drivers:**
- The "Intellectual Property" of Truth: The internet's fascination with Hedy Lamarr is already active. Viral articles, social media posts, and documentaries have primed the global audience for a high-budget dramatization of her life.
- The Golden Age Hook: Visually, the film offers double-value: the breathtaking glamour of 1930s/40s Hollywood fashion paired with the grittiness of wartime espionage.
- Dual-Acreage Appeal: The film offers two distinct acts that can be marketed separately: Act I (thrilling escape from Austria-Hollywood rise) and Act II (the intellectual partnership with the tragic, bitter-sweet scientific legacy).

**Risks & Mitigation Strategies:**
- Risk 1: The High Cost of Period Pieces: Designing 1930s Austria, 1940s Hollywood, 1960s Cuba-era military rooms, and 1990s tech eras can quickly balloon a budget. *Mitigation:* Keep the production budget strictly between $30M – $45M. Utilize tax-incentive locations (e.g., Eastern Europe for cost efficiency).

### System Overview
High-level view of how all components interact:

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
