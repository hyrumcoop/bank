from player import MCTSPlayer, RandomPlayer, NDoublesPlayer, NPotPlayer
from player.adversarial_leader import AdversarialLeader
from player.n_rolls_player import NRollsPlayer
from simulation import play_game

if __name__ == '__main__':
    # Run MCTS player against all other players in multiple games, keep track of win ratios

    num_sims = 1000
    players = [MCTSPlayer(num_simulations=100), RandomPlayer(), NPotPlayer(200), NPotPlayer(1000), NRollsPlayer(7), NRollsPlayer(14), NDoublesPlayer(3), NDoublesPlayer(7), AdversarialLeader()]
    wins = [0] * len(players)

    print([player.__class__.__name__ for player in players])

    for i in range(num_sims):
        results = play_game(players, total_rounds=3)
        winners = results.get_current_state().get_leaders()
        for winner in winners:
            wins[winner] += 1
    
    print('Win ratios:')
    for i, player in enumerate(players):
        print(f'Player {i+1}: {wins[i]}/{num_sims} ({wins[i]/num_sims:.2f})')

    