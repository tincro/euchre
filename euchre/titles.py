"""The titles module contains display functions.

title(): -- Print title screen.
congrats(): -- Print the winning team.
"""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from team import Team

# Print the title screen for the game
def title():
    """Print the title screen for the game."""
    print('-' * 40)
    print(f'\t\tEUCHRE')
    print('-' * 40)
    print(f'Welcome to the classic card game of Euchre!')
    print('\n')

# Congratulate the winners of the game
def congrats(team: Team):
    """Congratulate the winners for a great game!
    
    Keyword arguments:
    team: -- the team that won the game.
    """
    players = team.get_players()
    print(f'Team {team.get_name()} HAS WON THE GAME! CONGRATULATIONS {players[0]} and {players[1]}!')
    