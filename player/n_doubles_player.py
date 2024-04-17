from game import BankGame
from player.player import BankPlayer

class NDoublesPlayer(BankPlayer):
    '''
    A player that chooses to bank only when n doubles after the first 3 rolls have been rolled
    '''

    doubles_threshold: int # Number of doubles before bank
    doubles: int #

    def __init__(self, doubles_threshold=3):
        self.doubles_threshold = doubles_threshold
        self.doubles = 0
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        rolls = game.get_dice_roll_events_for_current_round()
        last_dice_roll = rolls[-1]
        if last_dice_roll.first == last_dice_roll.second and len(rolls) > 3:
            self.doubles += 1

        if self.doubles_threshold <= self.doubles:
            return True

        return False
