from typing import List
from .quest import Quest, Action, State


class StateMachine:
    """
    Manages the state of a running quest instance.
    """

    def __init__(self, quest_definition: Quest):
        self._quest = quest_definition
        self.current_state: State = None
        self.is_started: bool = False

    def start(self) -> None:
        """Initializes the state machine to the quest's initial state."""
        if self.is_started:
            raise RuntimeError("State machine has already been started.")

        initial_state_name = self._quest.initial_state
        if initial_state_name not in self._quest.states:
            raise ValueError(
                f"Initial state '{initial_state_name}' not found in quest definition."
            )

        self.current_state = self._quest.states[initial_state_name]
        self.is_started = True
        print(
            f"Quest '{self._quest.quest_name}' started. Current state: {self.current_state.name}"
        )

    def transition(self, on_event: str) -> bool:
        """
        Transitions the state machine to a new state based on an event.
        Returns True if the transition was successful, False otherwise.
        """
        if not self.is_started:
            raise RuntimeError("State machine must be started before transitioning.")

        for trans in self.current_state.transitions:
            if trans.on == on_event:
                next_state_name = trans.to
                if next_state_name not in self._quest.states:
                    raise ValueError(
                        f"Transition target state '{next_state_name}' not found."
                    )

                self.current_state = self._quest.states[next_state_name]
                print(
                    f"Transitioned on event '{on_event}'. New state: {self.current_state.name}"
                )
                return True

        print(
            f"No transition found for event '{on_event}' from state '{self.current_state.name}'."
        )
        return False

    def get_on_enter_actions(self) -> List[Action]:
        """Returns the list of actions to be executed for the current state."""
        if not self.is_started:
            return []
        return self.current_state.on_enter
