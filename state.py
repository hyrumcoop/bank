import random

from event import BankEvent, DecisionEvent, DiceRollEvent, GameCompleteEvent, RoundCompleteEvent

class BankState:
    '''
    Represents a single snapshot of a Bank game. Should be treated as immutable outside of this module.

    Attributes:
        num_players (int): The number of players in the game.
        total_rounds (int): The total number of rounds in the game.
        cur_round (int): The current round of the game.
        balances (list[int]): The balances of each player.
        pot (int): The amount of money in the pot.
        rolls (int): The number of rolls made in the current round.
        can_bank (list[bool]): A list indicating whether each player can bank.
        player (int): The current player.

    Methods:
        __init__(self, num_players: int, total_rounds: int): Initializes a new BankState object.
        is_terminal(self) -> bool: Checks if the game has reached a terminal state.
        get_leaders(self) -> list[int]: Gets the player(s) with the highest balance.
        copy(self): Creates a copy of the BankState object.

    '''

    def __init__(self, num_players: int, total_rounds: int):
        '''
        Initializes a new BankState object.

        Args:
            num_players (int): The number of players in the game.
            total_rounds (int): The total number of rounds in the game.

        '''
        
        self.num_players = num_players
        self.total_rounds = total_rounds
        self.cur_round = 0
        self.balances = [0] * num_players
        self.pot = 0
        self.rolls = 0
        self.can_bank = [True] * num_players
        self.player = 0
    
    def is_terminal(self) -> bool:
        '''
        Checks if the game has reached a terminal state.

        Returns:
            bool: True if the game is in a terminal state, False otherwise.

        '''

        return self.cur_round == self.total_rounds
    
    def get_leaders(self) -> list[int]:
        '''Gets the player(s) with the highest balance.'''

        max_balance = max(self.balances)
        return [i for i, balance in enumerate(self.balances) if balance == max_balance]

    def copy(self):
        '''
        Creates a copy of the BankState object.

        Returns:
            BankState: A new BankState object with the same attribute values as the original.

        '''

        new_state = BankState(self.num_players, self.total_rounds)
        new_state.cur_round = self.cur_round
        new_state.balances = self.balances.copy()
        new_state.pot = self.pot
        new_state.rolls = self.rolls
        new_state.can_bank = self.can_bank.copy()
        new_state.player = self.player
        return new_state

def next_state(state: BankState, bank: bool) -> tuple[BankState, list[BankEvent]]:
    '''
    Computes the next state of the game based on the current player's decision. The original state is not modified. A
    list of events is returned to indicate what occurred during the transition, such as dice rolls, player decisions,
    and round completions.

    Args:
        state (BankState): The current state of the bank game.
        bank (bool): The decision of the current player to bank or not.

    Returns:
        tuple[BankState, list[BankEvent]]: A tuple containing the next state of the bank game and a list of events that occurred during the transition.
    '''

    events: list[BankEvent] = []

    if state.is_terminal():
        return state, events

    state = state.copy()
    state, decision_event = _execute_decision(state, bank)
    events.append(decision_event)
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

def _execute_decision(state: BankState, bank: bool) -> tuple[BankState, DecisionEvent]:
    player = state.player

    if bank:
        state.balances[player] += state.pot
        state.can_bank[player] = False

        state.player = 0 # Reset decision to first player
    else:
        state.player += 1 # Let next player decide

    event = DecisionEvent(player, bank, state.balances[player])
    
    return state, event

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