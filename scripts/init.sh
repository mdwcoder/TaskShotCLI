#!/bin/bash

# TaskShotCLI Init Script for Linux/macOS

# Get the absolute path of the repo directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$REPO_DIR/src"

echo "Repo Dir: $REPO_DIR"

# Detect Shell RC file
RC_FILE=""
SHELL_NAME=$(basename "$SHELL")

if [ "$SHELL_NAME" = "zsh" ]; then
    RC_FILE="$HOME/.zshrc"
elif [ "$SHELL_NAME" = "bash" ]; then
    RC_FILE="$HOME/.bashrc"
    # Mac use .bash_profile sometimes, but .bashrc is safer generic
    if [ "$(uname)" = "Darwin" ] && [ ! -f "$HOME/.bashrc" ]; then
        RC_FILE="$HOME/.bash_profile"
    fi
else
    echo "Unknown default shell: $SHELL_NAME. Trying to guess."
    if [ -f "$HOME/.zshrc" ]; then
        RC_FILE="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        RC_FILE="$HOME/.bashrc"
    fi
fi

if [ -z "$RC_FILE" ]; then
    echo "Could not find a suitable shell configuration file (.bashrc/.zshrc)."
    echo "Please manually add the following alias to your shell config:"
    echo "alias tsk='PYTHONPATH=\"$SRC_DIR\" python3 -m tskcli.cli'"
    exit 1
fi

# Define Alias
# Using python3 -m tskcli.cli ensures relative imports work
# We set PYTHONPATH to src
ALIAS_CMD="alias tsk='PYTHONPATH=\"$SRC_DIR\" python3 -m tskcli.cli'"

echo "Adding alias to $RC_FILE..."

# Backup rc file
cp "$RC_FILE" "$RC_FILE.bak"

# Append alias
echo "" >> "$RC_FILE"
echo "# TaskShotCLI Alias" >> "$RC_FILE"
echo "$ALIAS_CMD" >> "$RC_FILE"

echo "Success! Added 'tsk' alias."
echo "Please run: source $RC_FILE"
echo "Or restart your terminal to use 'tsk'."
