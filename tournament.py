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

def run_tournament(games: int, table_size: int, rounds_per_game: int = 10) -> list[PlayerStats]:

    # Perform games games of randomly selected tables of table_size.
    # There will be one table for each available strategy, meaning that table_size players will implement a certain strategy
    # Randomly selected tables will be better than a round robin because it's not necessarily important that a certain
    # strategy plays every other strategy once, but rather that we see lots of different combinations of strategies and pit them against each other
    players: list[PlayerStats] = []

    emptyWinsVs: dict[type, int] = {
        'OpTwoPlayer': 0,
        'LastBankingPlayer': 0,
        '3DoublesPlayer': 0,
        '7DoublesPlayer': 0,
        '200PotPlayer': 0,
        '1000PotPlayer': 0,
        '7RollsPlayer': 0,
        '14RollsPlayer': 0,
        '1/3RandomPlayer': 0,
        '1/6RandomPlayer': 0,
        '1/12RandomPlayer': 0,
        'AdversarialLeader': 0,
        '1/2PlayersPlayer': 0
    }
    emptyPlacements: dict[int, int] = {}
    for i in range(table_size):
        emptyPlacements[i + 1] = 0

    absolutePlacement = {
        'OpTwoPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        'LastBankingPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        '200PotPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        '1000PotPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        '7RollsPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        '14RollsPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        '1/3RandomPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        '1/6RandomPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        '1/12RandomPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        '3DoublesPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        '7DoublesPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        'AdversarialLeader': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        },
        '1/2PlayersPlayer': {
            'winsVs': emptyWinsVs.copy(),
            'games_played': 0,
            'placements': emptyPlacements.copy()
        }
    }

    for i in range(table_size):
        players.append({
            'player': LastBankingPlayer(),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': 'OpTwoPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': LastBankingPlayer(),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': 'LastBankingPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': NPotPlayer(200),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': '200PotPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': NPotPlayer(1000),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': '1000PotPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': NDoublesPlayer(3),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': '3DoublesPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': NDoublesPlayer(7),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': '7DoublesPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': NRollsPlayer(7),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': '7RollsPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': NRollsPlayer(14),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': '14RollsPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': RandomPlayer(1 / 3),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': '1/3RandomPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': RandomPlayer(1 / 6),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': '1/6RandomPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': RandomPlayer(1 / 12),
            'winsVs': emptyWinsVs.copy(),
            'scores': [],
            'name': '1/12RandomPlayer',
            'placements': emptyPlacements.copy()
        })
        players.append({
            'player': AdversarialLeader(),
            'winsVs': emptyWinsVs,
            'scores': [],
            'name': 'AdversarialLeader',
            'placements': emptyPlacements
        })
        players.append({
            'player': NPlayersPlayer(floor(table_size / 2)),
            'winsVs': emptyWinsVs,
            'scores': [],
            'name': '1/2PlayersPlayer',
            'placements': emptyPlacements
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
    with open('results.csv', 'w') as csvfile:

        fieldnames = [
            'playerName', 
            'roundsPerGame', 
            'playersPerTable', 
            'winsVOpTwoPlayer',
            'winsV1/2PlayersPlayer',
            'winsV1/12RandomPlayer',
            'winsV1/3RandomPlayer',
            'winsV1/6RandomPlayer',
            'winsV1000PotPlayer',
            'winsV14RollsPlayer',
            'winsV200PotPlayer',
            'winsV3DoublesPlayer',
            'winsV7DoublesPlayer',
            'winsV7RollsPlayer',
            'winsVAdversarialLeader',
            'winsVLastBankingPlayer',
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

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        def addStatsToCSV(playerStandings: PlayerStats, players: int, rounds: int):
            jsonStart = { 
                'roundsPerGame': rounds,
                'playersPerTable': players
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

