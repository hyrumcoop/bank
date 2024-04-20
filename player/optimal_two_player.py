from game import BankGame
from player.player import BankPlayer

class OpTwoPlayer(BankPlayer):
    '''
    This player plays the optimal 2-player strategy. The player will never be the first to bank, but will immediately bank after the opposing
    player banks for the first time. From then on, this player will then just copy the opponent's moves. This should result in winning the
    game 5 out of 6 times.
    '''

    def __init__(self):
        self.otherPlayerBanked = False
        self.rollNumberOtherPlayerBanked = 0
        self.inFirst = False

    def get_decision(self, game: BankGame, player: int) -> bool:
        state = game.get_current_state()
        if(state.rolls == 1):
            self.inFirst = player in state.get_leaders() and len(state.get_leaders()) == 1

        # If player is in the lead, copy second place's move
        if self.inFirst:
            second = state.get_placements()[1]
            return not state.can_bank[second]
        
        # Otherwise, bank one roll after the first other player banks
        elif self.otherPlayerBanked and state.rolls > self.rollNumberOtherPlayerBanked:
            self.otherPlayerBanked = False
            return True
        
        # Take note of when other players are banking
        unbanked_players = 0
        for bankable in state.can_bank:
            if bankable:
                unbanked_players += 1

        if unbanked_players < state.num_players:
            self.otherPlayerBanked = True
            self.rollNumberOtherPlayerBanked = state.rolls

        return False
