from state import BankState, _next_dice_roll, next_state
from event import BankEvent

class BankGame:
    '''
    Represents an entire game of Bank, including a state history. Individual game states are immutable,
    but the game object itself is mutable and can be used to progress through the game.

    Attributes:
        state_history (list[BankState]): A list of all game states.
        decision_history (list[bool]): A list of all decisions made by the players.
        event_history (list[list[BankEvent]]): A list of all events that have occurred in the game.
    
    Methods:
        get_current_state: Returns the current state of the game.
        decide: Progresses the game by executing the current player's decision to bank or not.
    '''

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
        '''Progresses the game by executing the current player's decision to bank or not. Returns the new state and events.'''

        state = self.get_current_state()
        new_state, events = next_state(state, bank)

        self.state_history.append(new_state)
        self.decision_history.append(bank)
        self.event_history.append(events)

        return new_state, events

def wrap_state(state: BankState) -> BankGame:
    '''Wraps the given state in a BankGame object.'''

    game = BankGame(state.num_players, state.total_rounds)
    game.state_history = [state]

    return game