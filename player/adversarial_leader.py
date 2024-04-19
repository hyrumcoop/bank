from game import BankGame
from player.player import BankPlayer

class AdversarialLeader(BankPlayer):
    '''
    A more complex player. If the player is in first, they will always bank only when the
    second place player banks. If the player is not in first, then they bank one doubles after the
    player directly ahead of them banks (as a means of clawing their way up to first).
    '''

    def __init__(self):
        pass

    def get_decision(self, game: BankGame, player: int) -> bool:
        state = game.get_current_state()
        placements = state.get_placements()

        

        if player in state.get_leaders():
            second_place_player = placements[1]
            if not state.can_bank[second_place_player]:
                return True

            else:
                return False

        else:
            placement = placements.index(player)
            secondPlace = placements[placement - 1]
            last_dice_roll = game.get_dice_roll_events_for_current_round()[-1]

            if state.can_bank[secondPlace]:
                return False
            elif last_dice_roll.first == last_dice_roll.second:
                # Bank as soon as one more doubles is rolled
                return True
            
        return False
