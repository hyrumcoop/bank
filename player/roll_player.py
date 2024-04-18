import numpy as np
from game import BankGame
from player.player import BankPlayer

class RandomPlayer(BankPlayer):
    '''
    A player that chooses to bank after n rolls, regardless of the current pot value.
    '''

    n: float # Number of rolls after which the player banks

    def __init__(self, n=np.random.normal(13,5)):
        if n < 4:
            self.n = abs(n)*np.random.randint(10,20)
        else:
            self.n = n
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        state = game.get_current_state()
        rolls = state.rolls
        return rolls > self.n