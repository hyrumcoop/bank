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
        self.diceRollNumber = 0

    def get_decision(self, game: BankGame, player: int) -> bool:

        self.diceRollNumber += 1

        # If player is in the lead, copy second place's move
        if player.int == game.get_current_leader_id:
            second = state.get_placements()[1]
            return not state.can_bank[second]
        
        # Otherwise, bank one roll after the first other player banks
        elif self.otherPlayerBanked and self.diceRollNumber > self.rollNumberOtherPlayerBanked:
            self.otherPlayerBanked = False
            return True
        
        # Take note of when other players are banking
        unbanked_players = 0
        state = game.get_current_state()
        for bankable in state.can_bank:
            if bankable:
                unbanked_players += 1

        if unbanked_players < state.num_players():
            self.otherPlayerBanked = True
            self.rollNumberOtherPlayerBanked = self.diceRollNumber

        return False
