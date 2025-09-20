#!/bin/bash

# Function to handle SIGTERM
handle_sigterm() {
    echo "SIGTERM received, performing cleanup..."
    
    # Lock and logout Bitwarden CLI
    /opt/bitwarden/bw lock
    /opt/bitwarden/bw logout

    # Forward SIGTERM to the child process
    if [ -n "$child_pid" ]; then
        kill -TERM "$child_pid" 2>/dev/null
        wait "$child_pid"
    fi
    
    echo -e "\nCleanup complete. Exiting."
    exit 0
}

# Trap SIGTERM
trap 'handle_sigterm' SIGTERM

echo "Logging in..."
/opt/bitwarden/bw login --apikey

echo -e "\nStarting main process..."
/opt/bitwarden/bw serve --hostname all --disable-origin-protection &
child_pid=$!  # Capture the process ID

# Wait for the process to finish
wait "$child_pid"
