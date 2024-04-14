from game import BankGame
from player import BankPlayer

def play_game(players: list[BankPlayer], total_rounds=10, event_hook=lambda state, events: None):
    num_players = len(players)
    game = BankGame(num_players, total_rounds)
    state = game.get_current_state()

    # Capture initial dice roll event
    event_hook(state, game.event_history[0])

    while not state.is_terminal():
        bank = players[state.player].get_decision(game, state.player)
        state, events = game.decide(bank)

        event_hook(state, events)

    return game