from state import BankState, _next_dice_roll, next_state
from event import BankEvent, DiceRollEvent, RoundCompleteEvent

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

    def get_event_history(self) -> list[list[BankEvent]]:
        return self.event_history
    
    def get_dice_roll_events_for_current_round(self) -> list[DiceRollEvent]:
        dice_rolls: list[DiceRollEvent] = []
        for event_set in reversed(self.event_history):
            for event in reversed(event_set):
                if type(event) is RoundCompleteEvent:
                    dice_rolls.reverse()
                    return dice_rolls
                if type(event) is DiceRollEvent:
                    dice_rolls.append(event)
        dice_rolls.reverse()
        return dice_rolls
    
    def decide(self, bank: bool) -> tuple[BankState, list[BankEvent]]:
        '''Progresses the game by executing the current player's decision to bank or not. Returns the new state and events.'''

        state = self.get_current_state()
        new_state, events = next_state(state, bank)

        self.state_history.append(new_state)
        self.decision_history.append(bank)
        self.event_history.append(events)

        return new_state, events
