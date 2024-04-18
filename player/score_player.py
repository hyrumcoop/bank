import numpy as np
from game import BankGame
from player.player import BankPlayer

class RandomPlayer(BankPlayer):
    '''
    A player that chooses to bank after the pot reaches n, regardless of how many rolls have happened.
    '''

    n: float # Size of the pot required for the player to bank

    def __init__(self, n=np.random.normal(300,100)):
        if n < 0:
            self.n = np.random.random()*5000
        elif n < 100:
            self.n = abs(n)*10
        else:
            self.n = n
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        state = game.get_current_state()
        pot = state.pot
        return pot > self.n