#!/bin/bash

# Define file paths
REPO_ALIASES="$HOME/dotfiles/homefiles/.bash_aliases"
TARGET_ALIASES="$HOME/.bash_aliases"

echo "Starting dotfiles setup..."

# Check if a .bash_aliases file already exists in the home directory
if [ -f "$TARGET_ALIASES" ] || [ -L "$TARGET_ALIASES" ]; then
    echo "Existing .bash_aliases found. Backing up to .bash_aliases.bak..."
    mv "$TARGET_ALIASES" "${TARGET_ALIASES}.bak"
fi

# Create the symbolic link
echo "Creating symbolic link for .bash_aliases..."
ln -s "$REPO_ALIASES" "$TARGET_ALIASES"

