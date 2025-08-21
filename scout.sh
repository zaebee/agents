#!/bin/bash

# The Messenger Bee's Exoskeleton
# It takes one argument: the message to be delivered.

# The entire message is passed as the first argument, in quotes.
MESSAGE="$1"

if [ -z "$MESSAGE" ]; then
  echo "ERROR: No message provided to messenger bee."
  exit 1
fi

echo "Messenger Bee dispatched with a scroll."

# Pass the message to the Python core.
RESULT=$(python3 scout_logic.py "$MESSAGE")

# Record the result in our River of Memory.
echo "Scroll delivered to River of Memory."
echo "---" >> river_memory.log
echo "Message delivered on: $(date)" >> river_memory.log
echo "$RESULT" >> river_memory.log
echo "---" >> river_memory.log
