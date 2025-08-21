#!/bin/bash

# --- Helper Functions ---
# This file contains common helper functions for the hive-cli.

function show_usage() {
    echo "The Genesis Engine - The 'Connector' to the Hive."
    echo "Usage: hive-cli <command> [options]"
    echo ""
    echo "Commands:"
    echo "  hatch <codon_type> <component_name>  - Scaffolds a new component pattern."
    # echo "  spin cocoon <component_name>         - Adds a test suite to a component."
    echo ""
    echo "Run 'hive-cli <command> --help' for more information on a specific command."
}
