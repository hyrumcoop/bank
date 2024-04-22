import json
import numpy as np
import matplotlib.pyplot as plt
from typing import TypedDict
from player import BankPlayer, NDoublesPlayer, NPotPlayer, NRollsPlayer
from simulation import play_game

class PlayerStats(TypedDict):
    player: BankPlayer
    wins: int
    scores: list[int]
    name: int


def find_optimal_stop(games: int, n_players: int, player_type: str, rounds_per_game: int = 10) -> list[PlayerStats]:
    
    # Perform games with players of a certain type to determine which threshold
    # results in the optimal score.
    players: list[PlayerStats] = []

    for i in range(n_players):
        if player_type == "doubles":
            players.append({
                'player': NDoublesPlayer(i+1),
                'wins': 0,
                'scores': [],
                'name': i+1
            })
        elif player_type == "pot":
            players.append({
                'player': NPotPlayer(((i+1)*10)+100),
                'wins': 0,
                'scores': [],
                'name': ((i+1)*10)+100
            })
        elif player_type == "rolls":
            players.append({
                'player': NRollsPlayer(i+1),
                'wins': 0,
                'scores': [],
                'name': i+1
            })
        else:
            print("Error: Please specify either 'doubles', 'pot', or 'rolls' for the player type.")

    game_players: list[BankPlayer] = []
    for player in players:
            game_players.append(player['player'])
    
    for game in range(games):
        results = play_game(game_players, rounds_per_game)
        balances = results.get_current_state().balances
        for player_index in range(len(balances)):
            players[player_index]['scores'].append(balances[player_index])

        winner_index = np.argmax(balances)
        players[winner_index]['wins'] += 1

    player_names: list[str] = []
    wins: list[int] = []
    avg_scores: list[int] = []
    med_scores: list[int] = []
    for player_index in range(len(players)):
        player_names.append(players[player_index]['name'])
        wins.append(players[player_index]['wins'])
        avg_scores.append(np.average(players[player_index]['scores']))
        med_scores.append(np.median(players[player_index]['scores']))

    # plt.figure(figsize=(12,8))
    # plt.bar(x=player_names, height=wins)
    # plt.xticks(player_names)
    # plt.title(f"Wins by player strategy for {rounds_per_game} rounds with {n_players} players")
    # plt.xlabel(f"Player Strategy ({player_type.capitalize()})")
    # plt.ylabel("Number of wins")
    # plt.savefig(f'optimal_stop_graphs/{player_type[0]}{rounds_per_game}_{n_players}w.png')
    # plt.show()

    # plt.figure(figsize=(12,8))
    # plt.bar(x=player_names, height=scores)
    # plt.xticks(player_names)
    # plt.title(f"Average Score by player strategy for {rounds_per_game} rounds with {n_players} players")
    # plt.xlabel(f"Player Strategy ({player_type.capitalize()})")
    # plt.ylabel("Number of wins")
    # plt.savefig(f'optimal_stop_graphs/{player_type[0]}{rounds_per_game}_{n_players}s.png')
    # plt.show()
    
    final_results = {
        'type': player_type,
        'players': player_names,
        'wins': wins,
        'avg_scores': avg_scores,
        'med_scores': med_scores
    }
    return final_results

if __name__ == "__main__":
    n_players = [10,20,50,100]
    player_types = ['doubles', 'pot', 'rolls']
    rounds = [10,15,20]
    results = {
        'doubles': {
            10: {
                10: {},
                15: {},
                20: {},
            }
        },
        'pot': {
            10: {
                10: {},
                15: {},
                20: {},
            },
            20: {
                10: {},
                15: {},
                20: {},
            },
            50: {
                10: {},
                15: {},
                20: {},
            },
            100: {
                10: {},
                15: {},
                20: {},
            }
        },
        'rolls': {
            10: {
                10: {},
                15: {},
                20: {},
            },
            20: {
                10: {},
                15: {},
                20: {},
            },
            50: {
                10: {},
                15: {},
                20: {},
            },
            100: {
                10: {},
                15: {},
                20: {},
            }
        }
    }
    
    for t in player_types:
        for n in n_players:
            for r in rounds:
                print(f"{t}: {n} players {r} rounds", end="...")
                res = find_optimal_stop(games=2000, n_players=n, player_type=t, rounds_per_game=r)
                results[t][n][r] = res
                print(" Done!")
            if t == 'doubles': ## We don't care about more than 10 doubles, since this is highly unlikely
                break
    
    with open('optimal_stop.json', 'w') as json_file:
        json.dump(results, json_file)