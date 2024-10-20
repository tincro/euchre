"""
Constants module for the game of Euchre.
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
MAX_TRICKS = 5

# Generic names to use for player
BOTS = ["Cow", "Dog", "Cat", "Pig"]
