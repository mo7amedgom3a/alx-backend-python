#!/bin/bash

# Script to setup Python virtual environment

# Set virtual environment name
VENV_NAME="venv"

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment: $VENV_NAME"
python3 -m venv $VENV_NAME

# Check if virtual environment was created successfully
if [ ! -d "$VENV_NAME" ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "Virtual environment '$VENV_NAME' created successfully!"
echo "To activate it, run: source $VENV_NAME/bin/activate"
echo "To deactivate it, run: deactivate"