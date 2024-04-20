import csv
import pprint
from math import floor
from random import shuffle
from typing import TypedDict
from player import BankPlayer, OpTwoPlayer, NPlayersPlayer, AdversarialLeader, LastBankingPlayer, NDoublesPlayer, NPotPlayer, NRollsPlayer, RandomPlayer
from simulation import play_game

class PlayerStats(TypedDict):
    player: BankPlayer
    winsVs: dict[str, int]
    placements: dict[int, int]
    scores: list[int]
    name: str

pot_limits = [i for i in range(50,2000, 50)]

def run_tournament(games: int, table_size: int, rounds_per_game: int = 10) -> list[PlayerStats]:

    # Perform games games of randomly selected tables of table_size.
    # There will be one table for each available strategy, meaning that table_size players will implement a certain strategy
    # Randomly selected tables will be better than a round robin because it's not necessarily important that a certain
    # strategy plays every other strategy once, but rather that we see lots of different combinations of strategies and pit them against each other
    players: list[PlayerStats] = []

    emptyWinsVs: dict[str, int] = {}
    absolutePlacement = {}
    emptyPlacements: dict[int, int] = {}

    for i in range(table_size):
        emptyPlacements[i + 1] = 0

    for pot_limit in pot_limits:
        emptyWinsVs[str(pot_limit) + 'PotPlayer'] = 0

    for pot_limit in pot_limits:
        absolutePlacement[str(pot_limit) + 'PotPlayer'] = {
            'winsVs': emptyWinsVs.copy(),
            'placements': emptyPlacements.copy(),
            'games_played': 0
        }

    for i in range(table_size):
        for pot_limit in pot_limits:
            players.append({
                'player': NPotPlayer(pot_limit),
                'winsVs': emptyWinsVs.copy(),
                'scores': [],
                'name': str(pot_limit) + 'PotPlayer',
                'placements': emptyPlacements.copy()
            })

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
                placement = table_size 
                for i in range(len(balances)):
                    if i == player_index:
                        continue

                    if balances[player_index] >= balances[i]:
                        placement -= 1
                        table[player_index]['winsVs'][table[i]['name']] += 1
                        absolutePlacement[table[player_index]['name']]['winsVs'][table[i]['name']] += 1

                table[player_index]['placements'][placement] += 1
                absolutePlacement[table[player_index]['name']]['placements'][placement] += 1
                absolutePlacement[table[player_index]['name']]['games_played'] += 1

    pprint.pprint(absolutePlacement)
    return absolutePlacement

if __name__ == '__main__':
    with open('n_pot_results.csv', 'w') as csvfile:

        fieldnames = [
            'playerName', 
            'roundsPerGame', 
            'playersPerTable', 
            'placementIn1',
            'placementIn2',
            'placementIn3',
            'placementIn4',
            'placementIn5',
            'placementIn6',
            'placementIn7',
            'placementIn8',
            'placementIn9',
            'games_played'
        ]

        for pot_limit in pot_limits:
            fieldnames.append('winsV' + str(pot_limit) + 'PotPlayer')

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        def addStatsToCSV(playerStandings: PlayerStats, players: int, rounds: int):
            jsonStart = { 
                'roundsPerGame': rounds,
                'playersPerTable': players,
            }

            for key, value in playerStandings.items():
                json = jsonStart.copy()

                json['playerName'] = key
                json['games_played'] = value['games_played']
                for player, winsV in value['winsVs'].items():
                    json['winsV' + player] = winsV

                for placement, times in value['placements'].items():
                    json['placementIn' + str(placement)] = times

                writer.writerow(json)


        addStatsToCSV(run_tournament(1000, 3, 10), 3, 10)
        addStatsToCSV(run_tournament(1000, 4, 10), 4, 10)
        addStatsToCSV(run_tournament(1000, 5, 10), 5, 10)
        addStatsToCSV(run_tournament(1000, 6, 10), 6, 10)
        addStatsToCSV(run_tournament(1000, 7, 10), 7, 10)
        addStatsToCSV(run_tournament(1000, 8, 10), 8, 10)
        addStatsToCSV(run_tournament(1000, 9, 10), 9, 10)

        addStatsToCSV(run_tournament(1000, 3, 15), 3, 15)
        addStatsToCSV(run_tournament(1000, 4, 15), 4, 15)
        addStatsToCSV(run_tournament(1000, 5, 15), 5, 15)
        addStatsToCSV(run_tournament(1000, 6, 15), 6, 15)
        addStatsToCSV(run_tournament(1000, 7, 15), 7, 15)
        addStatsToCSV(run_tournament(1000, 8, 15), 8, 15)
        addStatsToCSV(run_tournament(1000, 9, 15), 9, 15)

        addStatsToCSV(run_tournament(1000, 3, 20), 3, 20)
        addStatsToCSV(run_tournament(1000, 4, 20), 4, 20)
        addStatsToCSV(run_tournament(1000, 5, 20), 5, 20)
        addStatsToCSV(run_tournament(1000, 6, 20), 6, 20)
        addStatsToCSV(run_tournament(1000, 7, 20), 7, 20)
        addStatsToCSV(run_tournament(1000, 8, 20), 8, 20)
        addStatsToCSV(run_tournament(1000, 9, 20), 9, 20)


