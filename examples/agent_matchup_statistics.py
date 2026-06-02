from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from knucklebones_ml import agents, env, logic


@dataclass
class SimulationHistory:
    game_id: list[int] = field(default_factory=list)
    turn_number: list[int] = field(default_factory=list)

    a1_score: list[int] = field(default_factory=list)
    a2_score: list[int] = field(default_factory=list)

    die: list[int] = field(default_factory=list)
    action: list[int | None] = field(default_factory=list)

    board: list[np.ndarray] = field(default_factory=list)

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "game_id": self.game_id,
                "turn_number": self.turn_number,
                "a1_score": self.a1_score,
                "a2_score": self.a2_score,
                "die": self.die,
                "action": self.action,
                "board": self.board,
            }
        )


def simulate_matchup(
    agent1: agents.Agent,
    agent2: agents.Agent,
    num_games: int = 1000,
    max_steps: int | None = None,
) -> SimulationHistory:
    """
    Simulate matches between two agents.

    Args:
        agent1 (agents.Agent): The first agent.
        agent2 (agents.Agent): The second agent.
        num_games (int, optional): The number of games to simulate.
            Must be at least 1. Defaults to 1000.

    Returns:
        SimulationHistory: An object containing the matchup results.

    """

    if num_games < 1:
        msg = "num_games must be at least 1"
        raise ValueError(msg)

    stats: SimulationHistory = SimulationHistory()
    game_env = env()

    options = {"max_steps": max_steps} if max_steps is not None else {}

    for game_id in range(num_games):
        game_env.reset(options=options)

        turn_number = 0
        agent1_dice = [0, 0, 0, 0, 0, 0]
        agent2_dice = [0, 0, 0, 0, 0, 0]

        last_state_saved = False

        for turn_number, agent in enumerate(game_env.agent_iter()):
            obs, _, terminated, truncated, _ = game_env.last()

            if terminated or truncated:
                action = None

            elif agent == "player_0":
                action = agent1.select_action(obs)
                agent1_dice[obs["die"] - 1] += 1
            else:
                action = agent2.select_action(obs)
                agent2_dice[obs["die"] - 1] += 1

            if action is None:
                print(f"Game {game_id} ended at turn {turn_number}.")

            if action is not None or not last_state_saved:
                stats.game_id.append(game_id)
                stats.turn_number.append(turn_number)

                scores = logic.evaluate_board_scores(obs["board"])
                stats.a1_score.append(scores[0])
                stats.a2_score.append(scores[1])

                stats.die.append(obs["die"])
                stats.action.append(action)
                stats.board.append(obs["board"])

                if action is None:
                    last_state_saved = True

            game_env.step(action)

    return stats


if __name__ == "__main__":
    agent1 = agents.RandomAgent()
    agent2 = agents.RandomAgent()

    stats = simulate_matchup(agent1, agent2, num_games=100)
    stats_df = stats.to_dataframe()

    print(stats_df.describe())
