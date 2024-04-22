from game import BankGame
from mcts.mcts import compute_mcts_decision
from player.player import BankPlayer
from player.reasonable_player import ReasonablePlayer

class MCTSPlayer(BankPlayer):
    '''A player that uses Monte Carlo Tree Search to make decisions.'''

    def __init__(self, num_simulations: int = 10):
        '''Initializes the MCTS player with the given number of simulations per decision.'''

        self.num_simulations = num_simulations
    
    def get_decision(self, game: BankGame, player: int) -> bool:
        if game.get_current_state().rolls < 3:
            return False # No risk in passing after the first two rolls

        return compute_mcts_decision(game.get_current_state(), self.num_simulations, rollout_player=ReasonablePlayer())