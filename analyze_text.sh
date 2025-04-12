#!/bin/bash

# Check if input file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <input_file.txt>"
    exit 1
fi

# Check if file exists
if [ ! -f "$1" ]; then
    echo "Error: File '$1' not found"
    exit 1
fi

# Get absolute path of input file
TEXT_FILE=$(realpath "$1")

echo "=== Combined Analysis Prompts ==="
echo ""
echo "1. Tone Analysis Prompt:"
echo "------------------------"
echo "# Tone Analysis"
echo "Text: <INSERT TEXT FROM $TEXT_FILE>"
echo "Language: en"
echo ""
echo "2. Concept Mapping Prompt (Portuguese):"
echo "-------------------------------------"
echo "# Concept Mapping"
echo "Text: <INSERT TEXT FROM $TEXT_FILE>"
echo "Language: pt"
echo ""
echo "3. Metaphor Analysis Prompt:"
echo "---------------------------"
echo "# Metaphor Analysis"
echo "Text: <INSERT TEXT FROM $TEXT_FILE>"
echo "Language: en"
echo ""
echo "=== End of Prompts ==="
echo ""
echo "Note: Replace <INSERT TEXT FROM $TEXT_FILE> with the actual content when using."
