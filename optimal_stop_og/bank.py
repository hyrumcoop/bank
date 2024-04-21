import numpy as np
from time import sleep
from player import Player

class Game:
    def __init__(self, num_players, show=False, method="pot"):
        self.pot = 0
        self.num_rolls = 0
        self.show = show
        self.get_players(num_players, method)
        self.highest_round = [0,0]
        self.round_totals = []

    def get_players(self,num_players, method):
        self.players = []
        for i in range(num_players):
            self.players.append(Player(i+1, show=self.show, method=method))

    def play_round(self, round_no):
        if self.show:
            print(f"Round #{round_no}")
        self.pot = 0
        self.num_rolls = 0
        while self.still_playing():
            self.num_rolls += 1
            d1 = np.random.randint(1,7)
            d2 = np.random.randint(1,7)
            total = d1 + d2
            if self.show:
                filler = " " if self.num_rolls < 10 else ""
                print(f"\tRoll {filler}#{self.num_rolls}: {d1} & {d2}", end="\t")
            if d1 == d2 and self.num_rolls > 3:
                self.pot *= 2
                if self.show:
                    print("Double!!")
            elif total == 7:
                if self.num_rolls <= 3:
                    self.pot += 70
                    if self.show:
                        print("Good 7!!")
                else:
                    if self.pot > self.highest_round[1]:
                        self.highest_round = [round_no, self.pot]
                    self.round_totals.append(self.pot)
                    self.pot = 0
                    if self.show:
                        print("It's all gone!")
                    break
            else:
                self.pot += total
            if self.show:
                print(f"\t\tThe pot is {self.pot}")
                sleep(0.1)
            for player in self.players:
                player.make_choice(self.pot, n_rolls=self.num_rolls)
            if self.show:
                sleep(0.5)
            if not self.still_playing():
                if self.pot > self.highest_round[1]:
                    self.highest_round = [round_no, self.pot]
                self.round_totals.append(self.pot)

    def play(self):
        for round_no in range(20):
            self.play_round(round_no+1)
            if self.show:
                sleep(0.25)
            self.reset_players()
        
        print("Results of game")
        winner = -1
        high_score = 0
        for player in self.players:
            if player.score > high_score:
                winner = player.index
                high_score = player.score
            fill = " " if player.index < 10 else ""
            print(f"\tPlayer {fill}{player.index} scored {str(player.score).center(4)} with threshold {player.criteria}.")
        print(f"Winner: Player {winner}")
        print(f"Highest scoring round: {self.highest_round[0]} with a pot of {self.highest_round[1]}")
        print("===Pot Stats===")
        print(f"Average Pot: {np.mean(self.round_totals)}")
        print(f"Median Pot: {np.median(self.round_totals)}")
        print(f"Min Pot: {np.min(self.round_totals)}")
        print(f"Q1 Pot: {np.quantile(self.round_totals, 0.25)}")
        print(f"Q3 Pot: {np.quantile(self.round_totals, 0.75)}")

    def still_playing(self):
        for player in self.players:
            if not player.banked:
                return True
        return False
    
    def reset_players(self):
        for player in self.players:
            player.banked = False