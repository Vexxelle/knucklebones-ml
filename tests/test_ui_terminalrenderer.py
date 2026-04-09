import sys
from io import StringIO
from unittest.mock import patch

import numpy as np

from knucklebones_ml.ui import BasicRenderer


def test_initialization():
    renderer = BasicRenderer(players=("Alice", "Bob"))
    assert renderer.players == ("Alice", "Bob")


def test_render_normal(sample_board_mixed):
    renderer = BasicRenderer(players=("Alice", "Bob"))
    renderer.last_die = 3  # Simulate the last die rolled
    obs = {"board": sample_board_mixed, "die": 3}
    player, last_action, terminated, truncated = "Alice", 1, False, False

    sys.stdout = StringIO()
    renderer.render(obs, player, last_action, terminated, truncated)

    expected_output = """\
Bob placed a 3 on column 2.

  ----------------------------------------  

Alice is up!
                 1   2   3                 
               ┌───┬───┬───┐  ╔═══════════╗
               │   │ 6 │ 3 │  ║   Alice   ║
               ├───┼───┼───┤  ║    53     ║
               │   │ 6 │ 3 │  ╬═══════════╬
               ├───┼───┼───┤  ║     3     ║
               │   │ 2 │ 3 │  ╚═══════════╝
               ┼───┼───┼───┼               
                 0  26  27                
                 0  16  16                
               ┼───┼───┼───┼               
╔═══════════╗  │   │ 4 │ 4 │               
║           ║  ├───┼───┼───┤               
╬═══════════╬  │   │ 4 │ 4 │               
║    Bob    ║  ├───┼───┼───┤               
║    32     ║  │   │   │   │               
╚═══════════╝  └───┴───┴───┘               
                 1   2   3                 

"""  # noqa: W291
    try:
        assert sys.stdout.getvalue() == expected_output
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout to default


def test_render_start_of_game(sample_board_empty):
    renderer = BasicRenderer(players=("Alice", "Bob"))
    obs = {"board": sample_board_empty, "die": 1}
    player, last_action, terminated, truncated = "Alice", None, False, False

    sys.stdout = StringIO()
    renderer.render(obs, player, last_action, terminated, truncated)

    expected_output = """\



  ========================================  

Knucklebones Game Started! Alice vs Bob

  ========================================  

Alice goes first! They rolled a 1.
                 1   2   3                 
               ┌───┬───┬───┐  ╔═══════════╗
               │   │   │   │  ║   Alice   ║
               ├───┼───┼───┤  ║     0     ║
               │   │   │   │  ╬═══════════╬
               ├───┼───┼───┤  ║     1     ║
               │   │   │   │  ╚═══════════╝
               ┼───┼───┼───┼               
                 0   0   0                
                 0   0   0                
               ┼───┼───┼───┼               
╔═══════════╗  │   │   │   │               
║           ║  ├───┼───┼───┤               
╬═══════════╬  │   │   │   │               
║    Bob    ║  ├───┼───┼───┤               
║     0     ║  │   │   │   │               
╚═══════════╝  └───┴───┴───┘               
                 1   2   3                 

"""  # noqa: W291
    try:
        assert sys.stdout.getvalue() == expected_output
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout to default


def test_render_game_over(sample_board_full):
    renderer = BasicRenderer(players=("Alice the Great", "Bob"))
    renderer.last_die = 3  # Simulate the last die rolled
    obs = {"board": sample_board_full, "die": 6}
    player, last_action, terminated, truncated = "Bob", 2, True, False

    sys.stdout = StringIO()
    renderer.render(obs, player, last_action, terminated, truncated)

    expected_output = """\
Alice the Great placed a 3 on column 3.

  ----------------------------------------  

                 1   2   3                 
               ┌───┬───┬───┐  ╔═══════════╗
               │ 1 │ 2 │ 3 │  ║Alice the _║
               ├───┼───┼───┤  ║    38     ║
               │ 4 │ 5 │ 6 │  ╬═══════════╬
               ├───┼───┼───┤  ║           ║
               │ 4 │ 3 │ 2 │  ╚═══════════╝
               ┼───┼───┼───┼               
                17  10  11                
                14  22  10                
               ┼───┼───┼───┼               
╔═══════════╗  │ 5 │ 5 │ 5 │               
║           ║  ├───┼───┼───┤               
╬═══════════╬  │ 3 │ 2 │ 1 │               
║    Bob    ║  ├───┼───┼───┤               
║    46     ║  │ 6 │ 5 │ 4 │               
╚═══════════╝  └───┴───┴───┘               
                 1   2   3                 


  ========================================  

               Game Over!               
        Bob wins with 46 points!        

  ========================================  



"""  # noqa: W291
    try:
        assert sys.stdout.getvalue() == expected_output
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout to default


def test_render_game_terminated_noflip(sample_board_mixed):
    renderer = BasicRenderer(players=("Alice", "Bob"), flip_board=False)
    renderer.last_die = 3  # Simulate the last die rolled
    obs = {"board": sample_board_mixed, "die": 6}
    player, last_action, terminated, truncated = "Bob", 2, False, True

    sys.stdout = StringIO()
    renderer.render(obs, player, last_action, terminated, truncated)

    expected_output_slice = """\

  ========================================  

            Game Truncated!             
       Alice wins with 53 points!       

  ========================================  



"""  # noqa: W291
    try:
        assert expected_output_slice in sys.stdout.getvalue()
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout to default


def test_user_input():
    renderer = BasicRenderer(players=("Alice", "Bob"))

    with patch("builtins.input", side_effect=["6", "Banana", "2", "3"]):
        expected_action = 2  # Function should keep asking until a valid input is given
        action = renderer.get_human_action("Alice", np.array([1, 0, 1]))

        assert action == expected_action
