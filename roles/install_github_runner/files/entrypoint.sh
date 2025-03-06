#!/bin/bash

# Fail on errors
set -e

# Check required variables
if [ -z "$GH_REPO_URL" ] || [ -z "$GH_RUNNER_TOKEN" ]; then
  echo "GH_REPO_URL and GH_RUNNER_TOKEN must be set!"
  exit 1
fi

# Cleanup on exit
cleanup() {
  echo "Removing runner..."
  ./config.sh remove --token $GH_RUNNER_TOKEN
}
trap cleanup EXIT

# Register the GitHub Runner
./config.sh --url "$GH_REPO_URL" --token "$GH_RUNNER_TOKEN" --unattended --name "$(hostname)" --work /home/github/_work

# Start the GitHub Runner
echo "Starting GitHub Actions Runner..."
./run.sh
