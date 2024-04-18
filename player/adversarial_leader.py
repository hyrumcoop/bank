from game import BankGame
from player.player import BankPlayer

class AdversarialLeader(BankPlayer):
    '''
    A more complex player. If the player is in first, they will always bank only when the
    second place player banks. If the player is not in first, then they bank either when the pot
    passes the score of the first player, or when the pot moves past n points
    '''

    def __init__(self):
        pass

    def get_decision(self, game: BankGame, player: int) -> bool:
        '''
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
        '''
        return True
