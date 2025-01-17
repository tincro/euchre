"""
Inputs module: allows us to get various input from the player that affect the
game directly.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.gui.interface import MainInterface

from PySide6.QtWidgets import QInputDialog

from docs.constants import BOTS
from random import sample

# Get Player names from the user, otherwise use bots.
def get_players(count: int, gui: MainInterface) -> list[str]:
    """Get player names from the user. Bots are used instead if chosen by the player.
    
    Keyword arguments:
    count: -- Number of players to create.
    """
    if not count:
        return
    
    names = []

    name_box = QInputDialog()
    text, ok = name_box.getText(gui, "New Player", "Player name:")
    if ok and text:
        gui.player_label.setText(f'Player: {text}')
    
    player_name = gui.player_label.text()
    names.append(player_name)

    bot_num = 3
    names.extend(sample(BOTS, bot_num))

    return names

def _enter_players(count: int) -> list[str]:
    players = []
    for i in range(count):
        name = input(f'Enter a name for Player {i+1}: ')
        while not name.isalnum():
            print(f'Invalid characters used. Please enter alpha numeric characters for name.')
            name = input(f'Enter a name for Player {i+1}: ')
        players.append(name)
    return players



