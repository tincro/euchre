"""
Constants module: holds constants for the game of Euchre.
"""
import sys

from PySide6.QtWidgets import QApplication

# User Interface
GUI = True
if len(sys.argv) == 1:
    # Check if we are using app if not don't initiate
    APP = QApplication()
else:
    APP = None

# General gameplay constants
PLAYER_COUNT = 4
TEAM_COUNT = 2
MAX_CARD_HAND_LIMIT = 5
POINTS_TO_WIN = 10
MIN_TRICKS = 3
MAX_TRICKS = 5

# Scoring
MIN_POINTS = 0
MAJORITY_POINTS = 1
MARCH_POINTS = 2
ALONE_POINTS = 4 

# Bot related
BOTS = ["Cow", "Dog", "Cat", "Pig"]
BOT_MAX = 3

# Quality of life
DELAY = True

