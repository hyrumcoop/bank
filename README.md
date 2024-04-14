# Bank

## Bank API Overview

This repo implements the Bank game logic as the foundation for the tournament ranking algorithm and Monte-Carlo tree search algorithm.

To simplify the player decision logic and Monte-Carlo tree search algorithm, the game is implemented as a turn-based game. After dice roll, each player is asked if they would like to bank. If a player chooses to bank, the decision process restarts, giving unbanked players a chance to change their mind based on the decision of others. The dice is rolled again once all players decide.

- `BankState`: Represents a single snapshot of a Bank game, containing all information needed to progress to the next state. This includes the current round number, the current player to decide, the pot amount, etc. The `BankState` objects should be treated as immutable.
- `BankGame`: Represents an entire Bank game, containing a history of previous states and events. Mutable, and can progress from state to state with the `BankGame.decide` method.
- `BankPlayer`: An abstract base class used to implement different Bank player strategies. The `BankPlayer.get_decision` method accepts a `BankGame` object, and makes a decision to bank or to pass given the current state of the game.
- `HumanPlayer`: An implementation of `BankPlayer`. Takes user input from the command-line. Useful for playing against computer strategies.
- `RandomPlayer`: Another implementation of `BankPlayer`. A basic strategy that randomly decides to bank with probability `p` regardless of the current game state, which is set in the constructor. Defaults to `p=0.25`.
- `next_state`: Returns the next state using the decision from the current player.
- `play_game`: Accepts a list of `BankPlayer`s, and simulates a game with the players until completion. The game is returned. The `event_hook` argument allows the caller to handle state and event updates after each decision.

## Usage

Running `python interactive.py` sets up an interactive game for a `HumanPlayer` against two `RandomPlayer`s.

