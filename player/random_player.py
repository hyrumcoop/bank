import random
from game import BankGame
from player.player import BankPlayer

class RandomPlayer(BankPlayer):
    '''
    A player that chooses to bank randomly, regardless of the current game state.
    '''

    p: float # Probability of banking

    def __init__(self, p=0.5):
        self.p = p
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        return random.random() < self.p