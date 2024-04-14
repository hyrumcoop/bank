from abc import ABC, abstractmethod
from game import BankGame

class BankPlayer(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_decision(self, game: BankGame, player: int) -> bool:
        '''
        Decide whether player should bank or not given the current game state. The entire game history is passed
        in case the player strategy depends on past decisions made by players.
        '''

        pass