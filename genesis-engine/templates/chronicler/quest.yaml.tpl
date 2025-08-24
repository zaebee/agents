# This is a sample quest definition for the ${ComponentName} chronicler.
# Edit this file to define the states, transitions, and actions for your quest.

quest_name: ${ClassName}Quest
initial_state: Start

states:
  Start:
    description: "The starting state of the quest."
    on_enter:
      - action: log_message
        params: { message: "Quest has started." }
    transitions:
      - to: Finish
        "on": "proceed"

  Finish:
    description: "The final state of the quest."
    on_enter:
      - action: log_message
        params: { message: "Quest has finished." }
