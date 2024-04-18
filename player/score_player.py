import numpy as np
from game import BankGame
from player.player import BankPlayer

class ScorePlayer(BankPlayer):
    '''
    A player that chooses to bank after the pot reaches a certain score.
    '''

    score: int # Size of the pot required for the player to bank

    def __init__(self, score=np.random.normal(300,100)):
        if score < 0:
            self.score = np.random.random()*5000
        elif score < 100:
            self.score = abs(n)*10
        else:
            self.score = score
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        state = game.get_current_state()
        pot = state.pot
        return pot > self.score