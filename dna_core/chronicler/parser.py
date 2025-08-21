import yaml
from pathlib import Path
from typing import Dict, Any
from .quest import Quest, State, Action, Transition

class QuestParser:
    """
    Parses a quest.yaml file into a structured Quest object.
    """

    def parse(self, file_path: Path) -> Quest:
        """
        Loads a YAML file and returns a Quest object.
        """
        if not file_path.is_file():
            raise FileNotFoundError(f"Quest file not found at: {file_path}")

        with open(file_path, 'r') as f:
            raw_data = yaml.safe_load(f)

        return self._create_quest_from_raw(raw_data)

    def _create_quest_from_raw(self, raw_data: Dict[str, Any]) -> Quest:
        """
        Constructs the Quest object from the raw dictionary loaded from YAML.
        """
        # Parse states
        parsed_states = {}
        for state_name, state_data in raw_data.get("states", {}).items():
            on_enter_actions = [Action(**action) for action in state_data.get("on_enter", [])]

            transitions = [Transition(**trans) for trans in state_data.get("transitions", []) if trans is not None]

            parsed_states[state_name] = State(
                name=state_name,
                description=state_data.get("description", ""),
                on_enter=on_enter_actions,
                transitions=transitions
            )

        # Create the final Quest object
        quest = Quest(
            quest_name=raw_data["quest_name"],
            initial_state=raw_data["initial_state"],
            states=parsed_states
        )

        return quest
