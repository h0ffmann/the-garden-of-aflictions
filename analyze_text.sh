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

# Read file content and escape special characters
TEXT_CONTENT=$(<"$1")
TEXT_CONTENT=${TEXT_CONTENT//$'\n'/\\n}
TEXT_CONTENT=${TEXT_CONTENT//\"/\\\"}

# Generate the combined prompts output
echo "=== Combined Analysis Prompts ==="
echo ""
echo "1. Tone Analysis Prompt:"
echo "------------------------"
echo "# Tone Analysis"
echo "Text: \"$TEXT_CONTENT\""
echo "Language: en"
echo ""
echo "2. Concept Mapping Prompt (Portuguese):"
echo "-------------------------------------"
echo "# Concept Mapping"
echo "Text: \"$TEXT_CONTENT\""
echo "Language: pt"
echo ""
echo "3. Metaphor Analysis Prompt:"
echo "---------------------------"
echo "# Metaphor Analysis"
echo "Text: \"$TEXT_CONTENT\""
echo "Language: en"
echo ""
echo "=== End of Prompts ==="
