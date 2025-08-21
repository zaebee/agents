from pathlib import Path
from dna_core.chronicler import QuestParser, StateMachine

class TestQuestChroniclerChronicler:
    """
    A Chronicler Bee that manages the 'test-quest-chronicler' quest.
    It loads a quest definition, runs a state machine, and executes actions.
    """

    def __init__(self):
        # Load the quest definition
        quest_path = Path(__file__).parent / "quest.yaml"
        self.quest_def = QuestParser().parse(quest_path)
        self.state_machine = StateMachine(self.quest_def)

        # Map action strings from YAML to methods on this class
        self.action_map = {
            "log_message": self.log_message,
            # --- Add other action mappings here ---
        }

    def run(self):
        """Starts the quest and executes the initial state's actions."""
        self.state_machine.start()
        self._execute_current_state_actions()

    def trigger_event(self, event: str):
        """Triggers a transition in the state machine."""
        transitioned = self.state_machine.transition(event)
        if transitioned:
            self._execute_current_state_actions()

    def _execute_current_state_actions(self):
        """Executes all on_enter actions for the current state."""
        actions = self.state_machine.get_on_enter_actions()
        for action in actions:
            if action.action in self.action_map:
                method = self.action_map[action.action]
                # Here you could add more sophisticated parameter handling
                method(**action.params)
            else:
                print(f"Warning: No method mapped for action '{action.action}'")

    # --- Action Implementations ---

    def log_message(self, message: str):
        """A simple example action that logs a message."""
        print(f"[Chronicler Log | {self.quest_def.quest_name}]: {message}")

    # --- Add other action methods here that correspond to your quest.yaml ---
