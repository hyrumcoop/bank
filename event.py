from typing import NamedTuple

type BankEvent = DiceRollEvent | RoundCompleteEvent | GameCompleteEvent

class DiceRollEvent(NamedTuple):
    first: int
    second: int
    pot: int

class RoundCompleteEvent(NamedTuple):
    round_number: int

class GameCompleteEvent:
    pass