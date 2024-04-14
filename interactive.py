from event import DiceRollEvent, GameCompleteEvent, RoundCompleteEvent
from game import BankGame
from player.human_player import HumanPlayer
from player.player import BankPlayer
from player.random_player import RandomPlayer

def play_game(players: list[BankPlayer], total_rounds=10):
    num_players = len(players)
    game = BankGame(num_players, total_rounds)
    state = game.get_current_state()

    print(f'The pot starts at {game.get_current_state().pot}\n')
    
    while not state.is_terminal():
        player = state.player
        bank = players[state.player].get_decision(game, state.player)
        state, events = game.decide(bank)

        if bank:
            print(f'Player {player} decided to bank')
            print(f'Player {player} now has {state.balances[player]} dollars\n')

        _print_events(events)
    
    return game

def _print_events(events):
    for event in events:
        if isinstance(event, DiceRollEvent):
            print(f'\nA {event.first} and a {event.second} were rolled')
            print(f'The pot is now {event.pot}\n')
        elif isinstance(event, RoundCompleteEvent):
            print(f'Round {event.round_number} is complete\n')
        elif isinstance(event, GameCompleteEvent):
            print('Game is complete')

if __name__ == '__main__':
    players = [HumanPlayer(), RandomPlayer(), RandomPlayer()]
    play_game(players, total_rounds=3)