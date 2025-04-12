#!/bin/bash

# Function to show all Portuguese prompts
show_pt_prompts() {
    for file in docs/prompts/*_pt.md; do
        cat "$file"
        echo ""
    done
    echo "THIS IS THE TEXT TO BE ANALYZED: "
}

# Main script logic
if [ "$1" == "--pt-prompts" ]; then
    show_pt_prompts
    exit 0
fi

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

# Function to extract prompt content
extract_prompt() {
    local file=$1
    awk '/^```python$/,/^```$/' "$file" | sed '1d;$d'
}

echo "=== Combined Analysis Prompts ==="
echo ""
echo "1. Tone Analysis Prompt:"
echo "------------------------"
extract_prompt "docs/prompts/analyze_tone_en.md"
echo ""
echo "Text: <INSERT TEXT FROM $TEXT_FILE>"
echo "Language: en"
echo ""
echo "2. Concept Mapping Prompt (Portuguese):"
echo "-------------------------------------"
extract_prompt "docs/prompts/concepts_map_pt.md"
echo ""
echo "Text: <INSERT TEXT FROM $TEXT_FILE>"
echo "Language: pt"
echo ""
echo "3. Metaphor Analysis Prompt:"
echo "---------------------------"
extract_prompt "docs/prompts/metaphor_analysis_en.md"
echo ""
echo "Text: <INSERT TEXT FROM $TEXT_FILE>"
echo "Language: en"
echo ""
echo "=== End of Prompts ==="
echo ""
echo "Note: Replace <INSERT TEXT FROM $TEXT_FILE> with the actual content when using."
