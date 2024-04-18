from game import BankGame
from player.player import BankPlayer

class NRollsPlayer(BankPlayer):
    '''
    A player that chooses to bank after n rolls
    '''

    rolls_threshold: int
    def __init__(self, rolls_threshold):
        self.rolls_threshold = rolls_threshold
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        rolls = game.get_dice_roll_events_for_current_round()
        if len(rolls) >= self.rolls_threshold:
            return True

        return False
