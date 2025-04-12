#!/bin/bash

#!/bin/bash

# Function to show all Portuguese prompts
show_pt_prompts() {
    for file in prompts/*_pt.prompt; do
        cat "$file"
        echo ""
    done
    echo "THIS IS THE TEXT TO BE ANALYZED: "
}

# Function to show prompt template
show_prompt() {
    local name=$1
    local lang=$2
    cat "prompts/${name}_${lang}.prompt"
    echo ""
    echo "Text: <INSERT TEXT HERE>"
    echo "Language: ${lang}"
    echo ""
}

# Main script logic
if [ "$1" == "--pt-prompts" ]; then
    show_pt_prompts
    exit 0
fi

if [ "$1" == "--all-prompts" ]; then
    echo "=== All Analysis Prompts ==="
    echo ""
    echo "1. Tone Analysis (English):"
    echo "--------------------------"
    show_prompt "analyze_tone" "en"
    
    echo "2. Concept Mapping (Portuguese):"
    echo "------------------------------"
    show_prompt "concepts_map" "pt"
    
    echo "3. Metaphor Analysis (English):"
    echo "-----------------------------"
    show_prompt "metaphor_analysis" "en"
    exit 0
fi

# Check if input file is provided
if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  $0 <input_file.txt>        - Analyze specific text file"
    echo "  $0 --pt-prompts            - Show all Portuguese prompts"
    echo "  $0 --all-prompts           - Show all analysis prompts"
    exit 1
fi

# Check if file exists
if [ ! -f "$1" ]; then
    echo "Error: File '$1' not found"
    exit 1
fi

# Get absolute path of input file
TEXT_FILE=$(realpath "$1")

echo "=== Text Analysis Setup ==="
echo ""
echo "File to analyze: $TEXT_FILE"
echo ""
echo "1. Copy one of these prompts:"
echo "   - analyze_tone_en"
echo "   - concepts_map_pt" 
echo "   - metaphor_analysis_en"
echo ""
echo "2. Replace <INSERT TEXT HERE> with content from:"
echo "   $TEXT_FILE"
echo ""
echo "Use './analyze_text.sh --all-prompts' to view all templates."
