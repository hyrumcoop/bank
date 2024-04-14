from game import BankGame
from player.player import BankPlayer

class ReasonablePlayer(BankPlayer):
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        state = game.get_current_state()

        # Don't consider banking until the dice has been rolled at least three times
        if state.rolls < 3:
            return False
        
        leaders = state.get_leaders()
        if player in leaders:
            # If we are in the lead, bank only when the next best player banks
            next_best_player = sorted(range(state.num_players), key=lambda x: state.balances[x], reverse=True)[1]

            # Side note: this means that the player will draw the game if player is a leader and uses this strategy
            return any([not state.can_bank[leader] for leader in leaders if leader != player])
        else:
            # If we are not in the lead, bank when the pot exceeds 97
            return state.pot >= 40