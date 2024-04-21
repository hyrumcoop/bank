import numpy as np
from player import Player

class Game_Sim:
    def __init__(self, num_players, method="pot"):
        self.get_players(num_players, method)
        self.pot = 0
        self.num_rolls = 0
        self.highest_round = [0,0]
        self.round_totals = []
        self.roll_stats = [[],[],[]]
        self.round_rolls = []
        self.winners = [[],[],[], []]

    def get_players(self, num_players, method):
        self.players = []
        for i in range(num_players):
            self.players.append(Player(i+1, method=method))

    def play_round(self, round_no):
        self.pot = 0
        self.num_rolls = 0
        while self.still_playing():
            self.num_rolls += 1
            d1 = np.random.randint(1,7)
            d2 = np.random.randint(1,7)
            total = d1 + d2
            self.roll_stats[0].append(total)
            self.roll_stats[1].append(d1)
            self.roll_stats[2].append(d2)
            if d1 == d2 and self.num_rolls > 3:
                self.pot *= 2
            elif total == 7:
                if self.num_rolls <= 3:
                    self.pot += 70
                else:
                    if self.pot > self.highest_round[1]:
                        self.highest_round = [round_no, self.pot]
                    self.round_totals.append(self.pot)
                    self.round_rolls.append(self.num_rolls)
                    self.pot = 0
                    break
            else:
                self.pot += total
            for player in self.players:
                player.make_choice(self.pot, n_rolls=self.num_rolls)
            if not self.still_playing():
                if self.pot > self.highest_round[1]:
                    self.highest_round = [round_no, self.pot]
                self.round_totals.append(self.pot)

    def play(self):
        self.get_players(len(self.players), method=self.players[0].method)
        for round_no in range(20):
            self.play_round(round_no+1)
            self.reset_players()
        
        winner = -1
        high_score = 0
        win_strat = 0
        win_method = "pot"
        for player in self.players:
            if player.score > high_score:
                winner = player.index
                high_score = player.score
                win_strat = player.criteria
                win_method = player.method
            # fill = " " if player.index < 10 else ""
            # print(f"\tPlayer {fill}{player.index} scored {str(player.score).center(5)} with threshold {player.criteria}.")
        
        self.winners[0].append(winner)
        self.winners[1].append(high_score)
        self.winners[2].append(win_method)
        self.winners[3].append(win_strat)

        # print(f"Winner: Player {winner}")
        # print(f"Highest scoring round: {self.highest_round[0]} with a pot of {self.highest_round[1]}")
        # print("===Pot Stats===")
        # print(f"Average Pot: {np.mean(self.round_totals)}")
        # print(f"Median Pot: {np.median(self.round_totals)}")
        # print(f"Min Pot: {np.min(self.round_totals)}")
        # print(f"Q1 Pot: {np.quantile(self.round_totals, 0.25)}")
        # print(f"Q3 Pot: {np.quantile(self.round_totals, 0.75)}")

    def get_stats(self):
        return self.round_rolls, self.roll_stats, self.round_totals, self.winners

    def still_playing(self):
        # for player in self.players:
        #     if not player.banked:
        #         return True
        # return False
        return True
    
    def reset_players(self):
        for player in self.players:
            player.banked = False