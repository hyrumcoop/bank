from state import BankState, _next_dice_roll, next_state
from event import BankEvent

class BankGame:
    state_history: list[BankState]
    decision_history: list[bool]
    event_history: list[list[BankEvent]]
    
    def __init__(self, num_players: int, total_rounds: int):
        state = BankState(num_players, total_rounds)
        
        # Begin game with first dice roll
        state, dice_event = _next_dice_roll(state)

        self.state_history = [state]
        self.decision_history = []
        self.event_history = [[dice_event]]
    
    def get_current_state(self) -> BankState:
        return self.state_history[-1]
    
    def decide(self, bank: bool) -> tuple[BankState, list[BankEvent]]:
        state = self.get_current_state()
        new_state, events = next_state(state, bank)

        self.state_history.append(new_state)
        self.decision_history.append(bank)
        self.event_history.append(events)

        return new_state, events