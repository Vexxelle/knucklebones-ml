import knucklebones_ml as kb


def main() -> None:
    # Player setup is not handled by the environment or renderer, so we define it here
    p1_name = input("\nEnter name for Player 1:\n").strip() or "Player 1"
    p2_name = input("\nEnter name for Player 2:\n").strip() or "Player 2"

    # Player names need to be mapped to agent names returned by the environment
    player_mapping = {"player_0": p1_name, "player_1": p2_name}

    # Create a terminal renderer instance
    player_names = (p1_name, p2_name)
    renderer = kb.ui.BasicRenderer(players=player_names)

    env = kb.env()
    env.reset()

    # The renderer needs to know the last action taken by the opponent to display it
    # None tells the renderer that the game is just starting
    last_action = None

    # Main game loop
    for agent in env.agent_iter():
        observation, _, terminated, truncated, _ = env.last()

        # Convert the agent name to the player name for rendering
        player_name = player_mapping[agent]

        renderer.render(
            obs=observation,
            player=player_name,
            last_action=last_action,
            terminated=terminated,
            truncated=truncated,
        )

        if terminated or truncated:
            continue

        # Get the current player's action
        action_mask = observation["action_mask"]
        action = renderer.get_human_action(player_name, action_mask)

        # Step the environment with the player's action
        env.step(action)

        # Update the last action for the next iteration
        last_action = action


if __name__ == "__main__":
    main()
