import random

from event import BankEvent, DiceRollEvent, GameCompleteEvent, RoundCompleteEvent

class BankState:
    
    # Game-scope state
    num_players: int
    total_rounds: int
    cur_round: int
    balances: list[int]

    # Round-scope state
    pot: int
    rolls: int
    can_bank: list[bool]
    player: int

    def __init__(self, num_players: int, total_rounds: int):
        self.num_players = num_players
        self.total_rounds = total_rounds
        self.cur_round = 0
        self.balances = [0] * num_players
        self.pot = 0
        self.rolls = 0
        self.can_bank = [True] * num_players
        self.player = 0
    
    def is_terminal(self) -> bool:
        return self.cur_round == self.total_rounds

    def copy(self):
        new_state = BankState(self.num_players, self.total_rounds)
        new_state.cur_round = self.cur_round
        new_state.balances = self.balances.copy()
        new_state.pot = self.pot
        new_state.rolls = self.rolls
        new_state.can_bank = self.can_bank.copy()
        new_state.player = self.player
        return new_state

def next_state(state: BankState, bank: bool) -> tuple[BankState, list[BankEvent]]:
    events: list[BankEvent] = []

    if state.is_terminal():
        return state, events

    state = state.copy()
    state = _execute_decision(state, bank)
    state = _rotate_decision(state)

    if state.player < state.num_players:
        # Players are still deciding
        return state, events
    
    # All players have decided

    if any(state.can_bank):
        # Some players can still bank; continue to next dice roll
        
        state, dice_event = _next_dice_roll(state)
        events.append(dice_event)

        if state.pot > 0:
            # Players begin decision-making again; begin with first player that can bank

            state.player = 0
            state = _rotate_decision(state) # Get first player that can bank

            return state, events
    
    # Round is over; continue to next round
    state, round_event = _next_round(state)
    events.append(round_event)

    if state.cur_round == state.total_rounds:
        # Game is over
        events.append(GameCompleteEvent())
        return state, events
    
    state, dice_event = _next_dice_roll(state)
    events.append(dice_event)

    return state, events

def _execute_decision(state: BankState, bank: bool) -> BankState:
    if bank:
        state.balances[state.player] += state.pot
        state.can_bank[state.player] = False

        state.player = 0 # Reset decision to first player
    else:
        state.player += 1 # Let next player decide
    
    return state

def _rotate_decision(state: BankState) -> BankState:
    # Find next player that can make decision
    while state.player < state.num_players and not state.can_bank[state.player]:
        state.player += 1
    
    return state

def _roll_dice() -> tuple[int, int]:
    return random.randint(1, 6), random.randint(1, 6)

def _next_pot_amount(dice: tuple[int, int], pot: int, rolls: int) -> int:
    dice1, dice2 = dice

    if rolls <= 3:
        if dice1 + dice2 == 7:
            return pot + 70
        else:
            return pot + dice1 + dice2
    else:
        if dice1 == dice2:
            return pot*2
        elif dice1 + dice2 == 7:
            return 0
        else:
            return pot + dice1 + dice2

def _next_dice_roll(state: BankState) -> tuple[BankState, DiceRollEvent]:
    dice = _roll_dice()
    state.rolls += 1
    state.pot = _next_pot_amount(dice, state.pot, state.rolls)

    event = DiceRollEvent(*dice, state.pot)

    return state, event

def _next_round(state: BankState) -> tuple[BankState, RoundCompleteEvent]:
    event = RoundCompleteEvent(state.cur_round)

    state.cur_round += 1
    state.rolls = 0
    state.pot = 0
    state.can_bank = [True] * state.num_players
    state.player = 0

    return state, event