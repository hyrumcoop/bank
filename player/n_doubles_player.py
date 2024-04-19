from game import BankGame
from player.player import BankPlayer

class NDoublesPlayer(BankPlayer):
    '''
    A player that chooses to bank only when n doubles after the first 3 rolls have been rolled
    '''

    doubles_threshold: int # Number of doubles before bank

    def __init__(self, doubles_threshold=3):
        self.doubles_threshold = doubles_threshold
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        rolls = game.get_dice_roll_events_for_current_round()
        last_dice_roll = rolls[-1]

        doubles = 0
        for roll in rolls[3:]:
            if roll.first == roll.second:
                doubles += 1


        if self.doubles_threshold <= doubles:
            return True

        return False
