from player import RandomPlayer, OpTwoPlayer, NPotPlayer
from simulation import play_game
import statistics

player1 = OpTwoPlayer()
player2 = OpTwoPlayer()

player1Scores = []
player2Scores = []
for game in range(1000):
    results = play_game([player1, player2], 15)
    scores = results.get_current_state().balances

    player1Scores.append(scores[0])
    player2Scores.append(scores[1])

print("Player 1 Score Mean")
print(player1Scores)
print(statistics.mean(player1Scores))
print("Player 2 Score Mean")
print(player2Scores)
print(statistics.mean(player2Scores))

player1 = OpTwoPlayer()
player2 = NPotPlayer(200)

player1Scores = []
player2Scores = []
for game in range(10000):
    results = play_game([player1, player2], 15)
    scores = results.get_current_state().balances

    player1Scores.append(scores[0])
    player2Scores.append(scores[1])

print("Player 1 Score Mean")
print(player1Scores)
print(statistics.mean(player1Scores))
print("Player 2 (Random) Score Mean")
print(player2Scores)
print(statistics.mean(player2Scores))

player1Wins = 0
for score_index in range(len(player1Scores)):
    if player1Scores[score_index] > player2Scores[score_index]:
        player1Wins += 1

print("Times followed by percentage of player one wins")
print(player1Wins)
print(player1Wins / 10000)

