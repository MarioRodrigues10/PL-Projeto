#!/bin/bash

# Check if autopep8 is installed
if ! command -v autopep8 &> /dev/null; then
    echo "Error: autopep8 is not installed. Please install autopep8."
    exit 1
fi

# Define the directory containing Python files
DIRECTORY="src"

# Format each Python file in the directory using autopep8
find "$DIRECTORY" -type f -name "*.py" -print0 | while IFS= read -r -d '' file; do
    if [[ "$(basename "$file")" != "parsetab.py" ]]; then
        echo "Formatting $file"
        autopep8 --in-place "$file"
    fi
done

echo "Formatting completed for all Python files in $DIRECTORY"
