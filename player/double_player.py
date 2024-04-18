import numpy as np
from game import BankGame
from player.player import BankPlayer

class RandomPlayer(BankPlayer):
    '''
    A player that chooses to bank after n doubles are rolled, regardless of the current pot value.
    '''

    n: float # Number of doubles rolled after which the player banks

    def __init__(self, n=np.random.normal(3,1)):
        if n < 1:
            self.n = abs(n)*np.random.randint(4,10)
        else:
            self.n = n
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        state = game.get_current_state()
        doubles = state.doubles
        return doubles >= self.n