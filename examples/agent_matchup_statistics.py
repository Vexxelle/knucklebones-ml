from pprint import pprint
from typing import Any

import numpy as np

from knucklebones_ml import agents, env, logic


def get_matchup_statistics(
    agent1: agents.Agent, agent2: agents.Agent, num_games: int = 1000
) -> dict[str, Any]:
    """
    Compute the matchup statistics between two agents.

    Args:
        agent1 (agents.Agent): The first agent.
        agent2 (agents.Agent): The second agent.
        num_games (int, optional): The number of games to simulate. Defaults to 1000.

    Returns:
        dict[str, float | int]: A dictionary containing the matchup statistics,
        including, for each agent:
            "agent1_wins", "draws", "total_games", "agent1_best_game",
            "agent1_average_winning_reward", "agent1_average_losing_reward",
            "agent1_winning_dice", "agent1_losing_dice", and the same for "agent2".

    """

    stats: dict[str, Any] = {
        "agent1_wins": 0,
        "agent2_wins": 0,
        "draws": 0,
        "total_games": num_games,
        "agent1_best_game": None,
        "agent2_best_game": None,
        "agent1_winning_dice": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
        "agent2_winning_dice": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
        "agent1_losing_dice": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
        "agent2_losing_dice": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
    }

    game_env = env()
    for _ in range(num_games):
        game_env.reset()

        rounds_played = 0
        agent1_dice = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        agent2_dice = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        last_board = np.array([])

        for agent in game_env.agent_iter():
            obs, _, terminated, truncated, _ = game_env.last()

            if terminated or truncated:
                last_board = obs["board"]
                action = None

            elif agent == "player_0":
                action = agent1.select_action(obs)
                rounds_played += 1
                agent1_dice[obs["die"]] += 1
            else:
                action = agent2.select_action(obs)
                agent2_dice[obs["die"]] += 1

            game_env.step(action)

        scores = logic.evaluate_board_scores(last_board)
        if scores[0] > scores[1]:
            stats["agent1_wins"] += 1

            if stats["agent1_best_game"] is None:
                stats["agent1_best_game"] = scores
            else:
                rel_score = scores[0] - scores[1]
                best_game = stats["agent1_best_game"]
                best_rel_score = best_game[0] - best_game[1]
                if rel_score > best_rel_score:
                    stats["agent1_best_game"] = scores

            for die_value in range(1, 6 + 1):
                stats["agent1_winning_dice"][die_value] += agent1_dice[die_value]
                stats["agent2_losing_dice"][die_value] += agent2_dice[die_value]

        elif scores[1] > scores[0]:
            stats["agent2_wins"] += 1

            if stats["agent2_best_game"] is None:
                stats["agent2_best_game"] = scores
            else:
                rel_score = scores[1] - scores[0]
                best_game = stats["agent2_best_game"]
                best_rel_score = best_game[1] - best_game[0]
                if rel_score > best_rel_score:
                    stats["agent2_best_game"] = scores

            for die_value in range(1, 6 + 1):
                stats["agent2_winning_dice"][die_value] += agent2_dice[die_value]
                stats["agent1_losing_dice"][die_value] += agent1_dice[die_value]

        else:
            stats["draws"] += 1

    return stats


def add_averaged_stats(stats: dict[str, Any]) -> dict[str, Any]:
    """
    Average out the statistics by the total number of games.

    Args:
        stats (dict[str, Any]): The statistics to average out.

    Returns:
        dict[str, Any]: stats + the averaged out statistics.
    """

    averaged_stats: dict[str, Any] = stats.copy()
    total_games = stats["total_games"]
    agent1_wins = stats["agent1_wins"]
    agent2_wins = stats["agent2_wins"]

    averaged_stats["agent1_win_rate"] = agent1_wins / total_games
    averaged_stats["agent2_win_rate"] = agent2_wins / total_games
    averaged_stats["draw_rate"] = stats["draws"] / total_games

    averaged_stats["agent1_averaged_winning_dice"] = {}
    averaged_stats["agent2_averaged_winning_dice"] = {}
    averaged_stats["agent1_averaged_losing_dice"] = {}
    averaged_stats["agent2_averaged_losing_dice"] = {}

    for die_value in range(1, 6 + 1):
        averaged_stats["agent1_averaged_winning_dice"][die_value] = (
            stats["agent1_winning_dice"][die_value] / agent1_wins
            if agent1_wins > 0
            else 0
        )
        averaged_stats["agent2_averaged_winning_dice"][die_value] = (
            stats["agent2_winning_dice"][die_value] / agent2_wins
            if agent2_wins > 0
            else 0
        )
        averaged_stats["agent1_averaged_losing_dice"][die_value] = (
            stats["agent1_losing_dice"][die_value] / agent2_wins
            if agent2_wins > 0
            else 0
        )
        averaged_stats["agent2_averaged_losing_dice"][die_value] = (
            stats["agent2_losing_dice"][die_value] / agent1_wins
            if agent1_wins > 0
            else 0
        )

    return averaged_stats


if __name__ == "__main__":
    agent1 = agents.RandomAgent()
    agent2 = agents.RandomAgent()

    stats = get_matchup_statistics(agent1, agent2, num_games=100)
    stats = add_averaged_stats(stats)

    pprint(stats)
