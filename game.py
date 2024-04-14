from bank import BankState, next_state

class BankGame:
    history: list[BankState]
    
    def __init__(self, num_players: int, total_rounds: int):
        self.history = [BankState(num_players, total_rounds)]
    
    def get_current_state(self) -> BankState:
        return self.history[-1]
    
    def decide(self, bank: bool):
        state = self.get_current_state()
        new_state = next_state(state, bank)
        self.history.append(new_state)