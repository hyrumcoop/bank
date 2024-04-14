from event import DecisionEvent, DiceRollEvent, GameCompleteEvent, RoundCompleteEvent
from simulation import play_game
from player import BankPlayer, RandomPlayer, HumanPlayer

def _print_events(state, events):
    for event in events:
        if isinstance(event, DiceRollEvent):
            print(f'\tA {event.first} and a {event.second} were rolled, giving a total of {event.first + event.second}.')
            print(f'\tThere are now {event.pot} dollars in the pot.\n')
        elif isinstance(event, DecisionEvent) and event.bank:
            print(f'\t\tPlayer {event.player+1} decided to bank.')
            print(f'\t\tPlayer {event.player+1} now has {event.balance} dollars.\n')
        elif isinstance(event, RoundCompleteEvent):
            print(f'Round {event.round_number+1} is complete.')
            print(f'Player balances: {state.balances}\n')
        elif isinstance(event, GameCompleteEvent):
            print('Game is complete.')
            leaders = state.get_leaders()
            if len(leaders) == 1:
                print(f'Player {leaders[0]+1} is the winner with {state.balances[leaders[0]]} dollars!')
            else:
                print(f'The game is a tie between players {", ".join(str(leader+1) for leader in leaders)}!')

if __name__ == '__main__':
    players: list[BankPlayer] = [HumanPlayer(), RandomPlayer(), RandomPlayer()]
    total_rounds = 3

    print(f'Beginning Bank with {len(players)} players and {total_rounds} rounds.\n')
    play_game(players, total_rounds=total_rounds, event_hook=_print_events)