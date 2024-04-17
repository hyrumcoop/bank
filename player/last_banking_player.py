from game import BankGame
from player.player import BankPlayer

class LastBankingPlayer(BankPlayer):
    '''
    A player that only banks after every single other player has banked and waits for one
    more double to be rolled
    '''

    def __init__(self):
        pass

    def get_decision(self, game: BankGame, player: int) -> bool:
        count = 0
        state = game.get_current_state()
        eventHistory = game.get_event_history()
        for bankable in state:
            if bankable:
                count += 1

        if count > 1:
            return False

        last_dice_roll = game.get_dice_roll_events_for_current_round()[-1]
        if last_dice_roll.first == last_dice_roll.second:
            # Bank as soon as one more doubles is rolled
            return True

        return False
        
        
