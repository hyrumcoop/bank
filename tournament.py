from random import shuffle
from typing import TypedDict
from player import BankPlayer, AdversarialLeader, LastBankingPlayer, NDoublesPlayer, NPotPlayer, NRollsPlayer, RandomPlayer
from simulation import play_game

class PlayerStats(TypedDict):
    player: BankPlayer
    winsVs: dict[str, int]
    placements: dict[int, int]
    scores: list[int]
    name: str

def run_tournament(games: int, table_size: int, rounds_per_game: int = 10):

    # Perform games games of randomly selected tables of table_size.
    # There will be one table for each available strategy, meaning that table_size players will implement a certain strategy
    # Randomly selected tables will be better than a round robin because it's not necessarily important that a certain
    # strategy plays every other strategy once, but rather that we see lots of different combinations of strategies and pit them against each other
    players: list[PlayerStats] = []

    emptyWinsVs: dict[type, int] = {
        'LastBankingPlayer': 0,
        '3DoublesPlayer': 0,
        '200PotPlayer': 0,
        '7RollsPlayer': 0,
        '1/6RandomPlayer': 0,
        #'AdversarialLeader': 0
    }
    emptyPlacements: dict[int, int] = {}
    for i in range(table_size):
        emptyPlacements[i + 1] = 0

    for i in range(table_size):
        players.append({
            'player': LastBankingPlayer(),
            'winsVs': emptyWinsVs,
            'scores': [],
            'name': 'LastBankingPlayer',
            'placements': emptyPlacements
        })
        players.append({
            'player': NDoublesPlayer(3),
            'winsVs': emptyWinsVs,
            'scores': [],
            'name': '3DoublesPlayer',
            'placements': emptyPlacements
        })
        players.append({
            'player': NPotPlayer(200),
            'winsVs': emptyWinsVs,
            'scores': [],
            'name': '200PotPlayer',
            'placements': emptyPlacements
        })
        players.append({
            'player': NRollsPlayer(7),
            'winsVs': emptyWinsVs,
            'scores': [],
            'name': '7RollsPlayer',
            'placements': emptyPlacements
        })
        players.append({
            'player': RandomPlayer(1 / 6),
            'winsVs': emptyWinsVs,
            'scores': [],
            'name': '1/6RandomPlayer',
            'placements': emptyPlacements
        })
        '''
        players.append({
            'player': AdversarialLeader(),
            'winsVs': emptyWinsVs,
            'scores': [],
            'name': 'AdversarialLeader',
            'placements': emptyPlacements
        })
        '''

    # Run our series of games with all of the players
    for game in range(games):
        tables: list[list[PlayerStats]] = []

        # Set up the tables
        shuffle(players)

        table_players: list[PlayerStats] = []
        for i in range(len(players)):
            if i != 0 and (i % table_size) == 0:
                tables.append(table_players)
                table_players = []

            table_players.append(players[i])

        tables.append(table_players)

        print(tables)

        # Run the game for each table
        for table in tables:
            game_players: list[BankPlayer] = []
            for player in table:
                game_players.append(player['player'])

            results = play_game(game_players, rounds_per_game)

            # Handle results
            balances = results.get_current_state().balances

            # Place and compare each player's score to the others
            for player_index in range(len(balances)):
                table[player_index]['scores'].append(balances[player_index])
                placement = 4
                for i in range(len(balances)):
                    if i == player_index:
                        continue

                    if balances[player_index] >= balances[i]:
                        placement -= 1
                        table[player_index]['winsVs'][table[i]['name']] += 1

                    table[player_index]['placements'][placement] += 1

    print(players)


if __name__ == '__main__':
    run_tournament(100, 4)
