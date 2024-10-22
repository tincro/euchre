"""
Constants module: holds constants for the game of Euchre.
"""
from euchre.cards import Card

# Card creation constants
VALUES = (9, 10, 11, 12, 13, 14)
SUITS = ("Spades", "Diamonds", "Clubs", "Hearts")
DECK = [
    Card(value, suit) for value in VALUES for suit in SUITS
]

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

# Generic names to use for player
BOTS = ["Cow", "Dog", "Cat", "Pig"]

DELAY = True
