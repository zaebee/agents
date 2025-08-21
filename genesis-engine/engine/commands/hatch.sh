#!/bin/bash
# The 'hatch' command - creates a new component from a codon template.

# Find the directory where the script is located to source helpers
SCRIPT_DIR=$(dirname "$0")
source "$SCRIPT_DIR/../config.sh"
source "$SCRIPT_DIR/../helpers.sh"

# --- Command-Specific Logic ---
CODON_TYPE=$1
COMPONENT_NAME=$2

if [ -z "$CODON_TYPE" ] || [ -z "$COMPONENT_NAME" ]; then
    echo "Error: 'hatch' requires a codon type and a component name."
    show_usage
    exit 1
fi

COMPONENT_PATH="$HIVE_ROOT/$COMPONENT_NAME"
echo "Hatching new '$CODON_TYPE' codon named '$COMPONENT_NAME'..."

if [ -d "$COMPONENT_PATH" ]; then
    echo "Error: Component '$COMPONENT_NAME' already exists at $COMPONENT_PATH."
    exit 1
fi

mkdir -p "$COMPONENT_PATH"
echo "Created directory: $COMPONENT_PATH"

case $CODON_TYPE in
    command)
        echo "Scaffolding 'Handle Command' pattern (C -> A -> G)..."
        touch "$COMPONENT_PATH/connector.py"
        touch "$COMPONENT_PATH/command.py"
        touch "$COMPONENT_PATH/aggregate.py"
        touch "$COMPONENT_PATH/event.py"
        ;;
    query)
        echo "Scaffolding 'Query Data' pattern (C -> T -> C)..."
        touch "$COMPONENT_PATH/connector.py"
        touch "$COMPONENT_PATH/query.py"
        touch "$COMPONENT_PATH/transformer.py"
        touch "$COMPONENT_PATH/dto.py"
        ;;
    event)
        echo "Scaffolding 'React to Event' pattern (G -> C -> A -> G)..."
        touch "$COMPONENT_PATH/listening_connector.py"
        touch "$COMPONENT_PATH/command.py"
        touch "$COMPONENT_PATH/aggregate.py"
        touch "$COMPONENT_PATH/new_event.py"
        ;;
    *)
        echo "Error: Unknown codon type '$CODON_TYPE'."
        rm -rf "$COMPONENT_PATH"
        show_usage
        exit 1
        ;;
esac

echo "Success! New '$CODON_TYPE' codon hatched at: $COMPONENT_PATH"
echo "Next steps: 'spin cocoon' to add tests."
