import numpy as np

class Player:
    def __init__(self, index, method="pot", show=False):
        self.index = index
        self.banked = False
        self.score = 0
        self.method = method
        self.show = show
        if self.method == "pot":
            self.criteria = max(int(np.random.normal(300,100)),100)
            if np.random.random() > 0.7:
                self.criteria *= max(int(np.random.normal(5,2)), 1)
        else:
            self.criteria = max(int(np.random.normal(15,5)),7)
            if np.random.random() > 0.9:
                self.criteria *= 2
            
    def make_choice(self, pot, n_rolls=0):
        if not self.banked:
            if self.method == "pot":
                if pot > self.criteria:
                    self.score += pot
                    self.banked = True
                    if self.show:
                        print(f"\tPlayer {self.index} banked.")
            else:
                if n_rolls > self.criteria:
                    self.score += pot
                    self.banked = True
                    if self.show:
                        print(f"\tPlayer {self.index} banked.")