
This is a Python implementation of the dice game **Knucklebones** from Cult of the Lamb with multiple AI player strategies.

## Game Mechanics

game.py implements the core game:
- **Board**: 3 rows per player, max 3 dice per row
- **Scoring**: Sum of (die value × count of that die in the row)
- **Placement**: Placing a die removes all opponent dice of the same value from that row
- **Win condition**: First player to fill all 9 slots (3 rows × 3 dice) ends the game, higher score wins

## Player Strategies

players.py contains 8 different AI implementations:

| Player | Strategy |
|--------|----------|
| **Human_Player** | Interactive console input |
| **Random_Player** | Random valid row selection |
| **Sequential_Player** | Always fills rows left to right |
| **Aggressive_Player** | Removes opponent dice aggressively |
| **Smart_Player** | Maximizes own score advantage |
| **Stupid_Player** | Minimizes own score (opposite of Smart) |
| **Combo_Player** | Prioritizes matching dice in own rows |
| **Pupser** | Complex heuristic combining deletion, combos, and scoring |

## Usage

- **main.py**: Interactive game mode (human vs bot or human vs human)
- **matchup_statistics.py**: Runs 10,000 matches between all player pairs and outputs win rates

The project helps analyze which AI strategies perform best against each other.