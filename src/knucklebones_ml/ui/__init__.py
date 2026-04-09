"""
UI components for the Knucklebones game.

This module defines the user interface classes for the Knucklebones game. It includes a
base class for the user interface and specific implementations.

"""

from knucklebones_ml.ui._base_class import BaseUI
from knucklebones_ml.ui._basic_terminal_ui import TerminalUI

__all__ = ["BaseUI", "TerminalUI"]
