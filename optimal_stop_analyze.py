import json
import matplotlib.pyplot as plt

with open('optimal_stop.json', 'r') as json_file:
    data = json.load(json_file)

print("Data loaded from optimal_stop.json")
# print("Dictionary:", data)
# print(data['doubles']['10']['10'])

n_players = ['10','20','50','100']
player_types = ['doubles', 'pot', 'rolls']
rounds = ['10','15','20']

for t in player_types:
    for n in n_players:
        for r in rounds:
            subset = data[t][n][r]
            plt.figure(figsize=(12,8))
            if subset['type'] == 'pot':
                plt.bar(x=subset['players'], height=subset['wins'], width=8)
            else:
                plt.bar(x=subset['players'], height=subset['wins'], width=0.8)
            title = "Number of Doubles" if subset['type'] == 'doubles' else "Number of Rolls" if subset['type'] == 'rolls' else "Pot Size"
            plt.title(f'Wins by {title} ({n} players {r} rounds)')
            plt.xlabel(title)
            plt.ylabel("Number of Wins (per 2000 games)")
            plt.savefig(f'optimal_stop_graphs/{t[0]}{r}_{n}w.png')
            # plt.show()

            plt.figure(figsize=(12,8))
            if subset['type'] == 'pot':
                plt.bar(x=subset['players'], height=subset['avg_scores'], label="Average", width=8)
                plt.bar(x=subset['players'], height=subset['med_scores'], label="Median", width=6)
            else:
                plt.bar(x=subset['players'], height=subset['avg_scores'], label="Average", width=0.8)
                plt.bar(x=subset['players'], height=subset['med_scores'], label="Median", width=0.6)
            plt.title(f'Scores by {title}  ({n} players {r} rounds)')
            plt.xlabel(title)
            plt.ylabel("Score per Game")
            plt.legend()
            plt.savefig(f'optimal_stop_graphs/{t[0]}{r}_{n}s.png')
            # plt.show()
        if t == 'doubles': ## We don't care about more than 10 doubles, since this is highly unlikely
                break