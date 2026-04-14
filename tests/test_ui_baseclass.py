import numpy as np
import pytest

from knucklebones_ml.ui import UserInterface


def test_same_player_names():
    error_message = "Player names must be unique."
    with pytest.raises(ValueError, match=error_message):
        UserInterface(players=("Alice", "Alice"))


def test_human_action_not_implemented():
    ui = UserInterface(players=("Alice", "Bob"))
    error_message = "The get_human_action method needs to be implemented by subclasses."
    with pytest.raises(NotImplementedError, match=error_message):
        ui.get_human_action(player="Alice", action_mask=np.array([1, 1, 1]))
