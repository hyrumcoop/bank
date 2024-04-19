from game import BankGame
from player.player import BankPlayer

class NPlayersPlayer(BankPlayer):
    '''
    A player that only banks after every single other player has banked and waits for one
    more double to be rolled
    '''

    players_threshold: int
    def __init__(self, players_threshold: int):
        self.players_threshold = players_threshold

    def get_decision(self, game: BankGame, player: int) -> bool:
        count = 0
        state = game.get_current_state()
        for bankable in state.can_bank:
            if bankable:
                count += 1

        if count > self.players_threshold:
            return False

        return True



