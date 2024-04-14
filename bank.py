import random

class BankState:
    
    # Game-scope state
    num_players: int
    total_rounds: int
    cur_round: int
    balances: list[int]

    # Round-scope state
    pot: int
    can_bank: list[bool]
    player: int

    def __init__(self, num_players: int, total_rounds: int):
        self.num_players = num_players
        self.total_rounds = total_rounds
        self.cur_round = 0
        self.balances = [0] * num_players
        self.pot = 0
        self.can_bank = [True] * num_players
        self.player = 0
    
    def is_terminal(self) -> bool:
        return self.cur_round == self.total_rounds

    def copy(self):
        new_state = BankState(self.num_players, self.total_rounds)
        new_state.cur_round = self.cur_round
        new_state.balances = self.balances.copy()
        new_state.pot = self.pot
        new_state.can_bank = self.can_bank.copy()
        new_state.player = self.player
        return new_state

def next_state(state: BankState, bank: bool) -> BankState:
    if state.is_terminal():
        return state

    state = _execute_decision(state.copy(), bank)
    state = _rotate_decision(state)

    if state.player < state.num_players:
        # Players are still deciding
        return state
    
    # All players have decided; time to re-roll dice
    state.player = 0
    dice = _roll_dice()
    state.pot = _next_pot_amount(dice, state.pot, state.cur_round)

    if state.pot > 0:
        # Players begin decision-making again
        return state
    
    # Round is over; continue to next round
    state.cur_round += 1
    state.can_bank = [True] * state.num_players
    
    dice = _roll_dice()
    state.pot = _next_pot_amount(dice, 0, state.cur_round)

    return state

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

def _next_pot_amount(dice: tuple[int, int], pot: int, round: int) -> int:
    dice1, dice2 = dice

    if round < 3:
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