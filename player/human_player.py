from game import BankGame
from player.player import BankPlayer

class HumanPlayer(BankPlayer):
    '''
    A player that asks the user for input to make decisions.
    '''

    def get_decision(self, game: BankGame, player: int) -> bool:
        while True:
            decision = input(f'Player {player}, do you want to bank? (y/n) ').strip().lower()
            if decision == 'y':
                return True
            elif decision == 'n':
                return False
            else:
                print('Invalid input. Please enter "y" or "n".')