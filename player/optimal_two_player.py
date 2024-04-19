from game import BankGame
from player.player import BankPlayer

class OpTwoPlayer(BankPlayer):
    '''
    This player plays the optimal 2-player strategy. The player will never be the first to bank, but will immediately bank after the opposing
    player banks for the first time. From then on, this player will then just copy the opponent's moves. This should result in winning the
    game 5 out of 6 times.
    '''

    def __init__(self):
        pass

    def get_decision(self, game: BankGame, player: int) -> bool:

        # If player is in the lead, copy second place's move
        if player.int == game.get_current_leader_id:
            return secondplace
        
        unbanked = 0
        state = game.get_current_state()
        for bankable in state.can_bank:
            if bankable:
                unbanked += 1

        # Otherwise, bank one roll after the first other player banks
        if unbanked < state.num_players():
            return True

        last_dice_roll = game.get_dice_roll_events_for_current_round()[-1]
        if last_dice_roll.first == last_dice_roll.second:
            # Bank as soon as one more doubles is rolled
            return True

        return False
