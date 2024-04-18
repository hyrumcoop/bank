from game import BankGame
from player.player import BankPlayer

class NPotPlayer(BankPlayer):
    '''
    A player that chooses to bank only when the pot reaches n points
    '''

    points_threshold: int # Number of doubles before bank

    def __init__(self, points_threshold):
        self.points_threshold = points_threshold
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        state = game.get_current_state()
        if state.pot >= self.points_threshold:
            return True

        return False
