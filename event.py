from typing import NamedTuple

type BankEvent = DiceRollEvent | DecisionEvent | RoundCompleteEvent | GameCompleteEvent

class DiceRollEvent(NamedTuple):
    first: int
    second: int
    pot: int

class DecisionEvent(NamedTuple):
    player: int
    bank: bool
    balance: int

class RoundCompleteEvent(NamedTuple):
    round_number: int

class GameCompleteEvent:
    pass
