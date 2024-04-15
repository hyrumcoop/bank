from dataclasses import dataclass
import math
import random
from game import wrap_state
from player.player import BankPlayer
from player.random_player import RandomPlayer
from state import BankState, next_state

type MCTSPlayerDecision = tuple[int, bool] # Player number after decision, decision (bank is True, pass is False)

@dataclass
class MCTSNode:
    parent: 'MCTSNode | None'
    player: int
    visits: int
    wins: float # float to account for draws, which are divided across the number of players who drew
    children: dict[MCTSPlayerDecision, 'MCTSNode']

def compute_mcts_decision(state: BankState, num_simulations: int = 10, rollout_player: BankPlayer = RandomPlayer()) -> bool:
    root = MCTSNode(parent=None, player=state.player, visits=0, wins=0, children={})

    # Run simulations
    for _ in range(num_simulations):
        mcts_simulation(state, root, rollout_player=rollout_player)

    # Choose node with max visits
    best_edge = max(root.children, key=lambda edge: root.children[edge].visits)

    return best_edge[1]

def mcts_simulation(state: BankState, node: MCTSNode, *, rollout_player: BankPlayer):
    '''Performs a single simulation of Open Loop MCTS on the given state and tree.'''

    if len(node.children) == 0:
        if state.is_terminal():
            score = _get_reward(state)
        else:
            # Expansion
            _expand_node(node, state)
            
            # Choose a random child to simulate
            edge, n_state = _choose_random_edge(state)

            # Simulation
            score = _rollout(n_state, player=rollout_player)

            # Backpropagation on child node
            node.children[edge].visits += 1
            node.children[edge].wins += score[edge[0]]
    else:
        # Otherwise, call recursively on child with highest value
        edge, n_state = _choose_best_edge(state, node)
        score = mcts_simulation(n_state, node.children[edge], rollout_player=rollout_player)

    # Backpropagation on current node
    node.visits += 1
    node.wins += score[node.player]

    return score

def _expand_node(node: MCTSNode, state: BankState):
    '''Expands the given node by adding all possible children.'''

    for player in range(state.num_players):
        node.children[(player, True)] = MCTSNode(parent=node, player=player, visits=0, wins=0, children={})
        node.children[(player, False)] = MCTSNode(parent=node, player=player, visits=0, wins=0, children={})

def _get_next_players(state: BankState) -> tuple[int, int]:
    '''Gets the player that will make the next decision in the given state. Returns
    a tuple of the player number after passing, and the player number after banking.'''

    pass_next_player = next_state(state, False)[0].player
    bank_next_player = next_state(state, True)[0].player

    return (pass_next_player, bank_next_player)

def _choose_random_edge(state: BankState) -> tuple[MCTSPlayerDecision, BankState]:
    '''Chooses a random MCTS tree edge from the given state.'''

    pass_state, bank_state = next_state(state, False)[0], next_state(state, True)[0]
    pass_edge, bank_edge = (pass_state.player, False), (bank_state.player, True)

    return random.choice([(pass_edge, pass_state), (bank_edge, bank_state)])

def _choose_best_edge(state: BankState, node: MCTSNode) -> tuple[MCTSPlayerDecision, BankState]:
    '''Chooses the best MCTS tree edge from the given state and node.'''

    pass_state, bank_state = next_state(state, False)[0], next_state(state, True)[0]
    pass_edge, bank_edge = (pass_state.player, False), (bank_state.player, True)

    pass_score, bank_score = uct(node.children[pass_edge]), uct(node.children[bank_edge])

    if pass_score > bank_score:
        return pass_edge, pass_state
    else:
        return bank_edge, bank_state

def uct(node: MCTSNode, c: float = math.sqrt(2)) -> float:
    '''Computes the UCT value of the given node.'''

    if node.visits == 0:
        return math.inf

    exploit_term = node.wins / node.visits

    if node.parent is None:
        explore_term = 0
    else:
        explore_term = c * (math.log(node.parent.visits) / node.visits) ** 0.5

    return exploit_term + explore_term

def _get_reward(state: BankState) -> list[float]:
    '''Gets the reward for each player in the given state.'''

    leaders = state.get_leaders()
    num_leaders = len(leaders)
    reward = 1 / num_leaders

    rewards: list[float] = [0] * state.num_players
    for leader in leaders:
        rewards[leader] = reward
    
    return rewards

def _rollout(state: BankState, player: BankPlayer) -> list[float]:
    '''Performs a rollout simulation of the game from the given state.'''

    while not state.is_terminal():
        decision = player.get_decision(wrap_state(state), state.player)
        state, _ = next_state(state, decision)

    return _get_reward(state)