from bank import BankState, next_state
from event import BankEvent

class BankGame:
    state_history: list[BankState]
    decision_history: list[bool]
    event_history: list[list[BankEvent]]
    
    def __init__(self, num_players: int, total_rounds: int):
        self.state_history = [BankState(num_players, total_rounds)]
        self.decision_history = []
        self.event_history = []
    
    def get_current_state(self) -> BankState:
        return self.state_history[-1]
    
    def decide(self, bank: bool) -> tuple[BankState, list[BankEvent]]:
        state = self.get_current_state()
        new_state, events = next_state(state, bank)

        self.state_history.append(new_state)
        self.decision_history.append(bank)
        self.event_history.append(events)

        return new_state, events