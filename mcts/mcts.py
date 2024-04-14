from dataclasses import dataclass
import math
import random
from state import BankState, next_state

type MCTSPlayerDecision = tuple[int, bool] # Player number after decision, decision (bank is True, pass is False)

@dataclass
class MCTSNode:
    parent: 'MCTSNode | None'
    player: int
    visits: int
    wins: float # float to account for draws, which are divided across the number of players who drew
    children: dict[MCTSPlayerDecision, 'MCTSNode']

def compute_mcts_decision(state: BankState, num_simulations: int = 10) -> bool:
    root = MCTSNode(parent=None, player=state.player, visits=0, wins=0, children={})

    # Run simulations
    for _ in range(num_simulations):
        mcts_simulation(state, root)

    # Choose node with max visits
    best_edge = max(root.children, key=lambda edge: root.children[edge].visits)

    return best_edge[1]

def mcts_simulation(state: BankState, node: MCTSNode):
    '''Performs a single simulation of Open Loop MCTS on the given state and tree.'''

    if len(node.children) == 0:
        # Expansion
        _expand_node(node, state)
        
        # Choose a random child to simulate
        edge = _choose_random_edge(state)

        # Simulation
        n_state = next_state(state, edge[1])[0]
        score = _rollout(n_state)

        # Backpropagation on child node
        node.children[edge].visits += 1
        node.children[edge].wins += score[node.player]
    else:
        # Otherwise, call recursively on child with highest value
        edge = _choose_best_edge(state, node)
        n_state = next_state(state, edge[1])[0]
        score = mcts_simulation(n_state, node.children[edge])

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

def _choose_random_edge(state: BankState) -> MCTSPlayerDecision:
    '''Chooses a random MCTS tree edge from the given state.'''

    pass_next_player, bank_next_player = _get_next_players(state)

    return random.choice([(pass_next_player, False), (bank_next_player, True)])

def _choose_best_edge(state: BankState, node: MCTSNode) -> MCTSPlayerDecision:
    '''Chooses the best MCTS tree edge from the given state and node.'''

    pass_next_player, bank_next_player = _get_next_players(state)
    pass_score, bank_score = uct(node.children[(pass_next_player, False)]), uct(node.children[(bank_next_player, True)])

    if pass_score > bank_score:
        return (pass_next_player, False)
    else:
        return (bank_next_player, True)

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

def _rollout(state: BankState) -> list[float]:
    '''Performs a rollout simulation of the game from the given state.'''

    while not state.is_terminal():
        state, _ = next_state(state, random.choice([True, False]))

    return _get_reward(state)