import random
from game import BankGame
from player.player import BankPlayer

class RandomPlayer(BankPlayer):
    '''
    A player that chooses to bank randomly with probability p, regardless of the current game state.
    '''

    p: float # Probability of banking

    def __init__(self, p=0.25):
        self.p = p
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        rolls = game.get_dice_roll_events_for_current_round()
        if len(rolls) <= 3:
            return False
        return random.random() < self.p

