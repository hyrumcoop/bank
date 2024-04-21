import numpy as np
from bank import Game
from bank_sim import Game_Sim
import matplotlib.pyplot as plt

def play():
    game = Game(10, method="len", show=True)

    for i in range(10):
        game.play()

def sim():
    game = Game_Sim(100, method="len")


    for i in range(1000):
        game.play()

    round_rolls, roll_stats, round_totals, winners = game.get_stats()
    print("\n===== Round Length Stats =====")
    print(f"Average Length: {np.mean(round_rolls)}")
    print(f"Median Length: {np.median(round_rolls)}")
    print(f"Min Length: {np.min(round_rolls)}")
    print(f"Q1 Length: {np.quantile(round_rolls, 0.25)}")
    print(f"Q3 Length: {np.quantile(round_rolls, 0.75)}")
    print(f"Max Length: {np.max(round_rolls)}")
    # print("\n===== Roll Total Stats =====")
    # print(f"Average Total: {np.mean(roll_stats[0])}")
    # print(f"Median Total: {np.median(roll_stats[0])}")
    # print(f"Min Total: {np.min(roll_stats[0])}")
    # print(f"Q1 Total: {np.quantile(roll_stats[0], 0.25)}")
    # print(f"Q3 Total: {np.quantile(roll_stats[0], 0.75)}")
    # print(f"Max Total: {np.max(roll_stats[0])}")
    # print("\n===== Roll (Die 1) Stats =====")
    # print(f"Average D1 Result: {np.mean(roll_stats[1])}")
    # print(f"Median D1 Result: {np.median(roll_stats[1])}")
    # print(f"Min D1 Result: {np.min(roll_stats[1])}")
    # print(f"Q1 D1 Result: {np.quantile(roll_stats[1], 0.25)}")
    # print(f"Q3 D1 Result: {np.quantile(roll_stats[1], 0.75)}")
    # print(f"Max D1 Result: {np.max(roll_stats[1])}")
    # print("\n===== Roll (Die 2) Stats =====")
    # print(f"Average D2 Result: {np.mean(roll_stats[2])}")
    # print(f"Median D2 Result: {np.median(roll_stats[2])}")
    # print(f"Min D2 Result: {np.min(roll_stats[2])}")
    # print(f"Q1 D2 Result: {np.quantile(roll_stats[2], 0.25)}")
    # print(f"Q3 D2 Result: {np.quantile(roll_stats[2], 0.75)}")
    # print(f"Max D2 Result: {np.max(roll_stats[2])}")
    print("\n===== Round Pot Stats =====")
    print(f"Average Pot: {np.mean(round_totals)}")
    print(f"Median Pot: {np.median(round_totals)}")
    print(f"Min Pot: {np.min(round_totals)}")
    print(f"Q1 Pot: {np.quantile(round_totals, 0.25)}")
    print(f"Q3 Pot: {np.quantile(round_totals, 0.75)}")
    print(f"Max Pot: {np.max(round_totals)}")
    print("\n===== High Score Stats =====")
    print(f"Average High Score: {np.mean(winners[1])}")
    print(f"Median High Score: {np.median(winners[1])}")
    print(f"Min High Score: {np.min(winners[1])}")
    print(f"Q1 High Score: {np.quantile(winners[1], 0.25)}")
    print(f"Q3 High Score: {np.quantile(winners[1], 0.75)}")
    print(f"Max High Score: {np.max(winners[1])}")
    print("\n===== Winning Threshold Stats =====")
    print(f"Average Threshold: {np.mean(winners[3])}")
    print(f"Median Threshold: {np.median(winners[3])}")
    print(f"Min Threshold: {np.min(winners[3])}")
    print(f"Q1 Threshold: {np.quantile(winners[3], 0.25)}")
    print(f"Q3 Threshold: {np.quantile(winners[3], 0.75)}")
    print(f"Max Threshold: {np.max(winners[3])}")

    plt.hist(winners[3], bins=np.linspace(7,np.max(winners[3]),np.max(winners[3])-6), rwidth=0.7)
    plt.xticks(np.linspace(7,np.max(winners[3]),np.max(winners[3])-6))
    plt.show()

sim()