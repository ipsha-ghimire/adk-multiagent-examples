#!/usr/bin/env bash
set -euo pipefail

# Small helper to run the workflow example using a local .env
if [ -f ".env" ]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' .env | xargs)
fi

python adk_multiagent_systems/workflow_agents/agent.py
