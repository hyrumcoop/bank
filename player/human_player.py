from game import BankGame
from player.player import BankPlayer

class HumanPlayer(BankPlayer):
    '''
    A player that asks the user for input to make decisions.
    '''

    def get_decision(self, game: BankGame, player: int) -> bool:
        while True:
            decision = input(f'\t\tPlayer {player+1}, do you want to bank? (y/n) ').strip().lower()
            if decision in ['y', 'n']:
                print()
                return decision == 'y'
            else:
                print('\t\tInvalid input. Please enter "y" or "n".')