"""The titles module contains display functions.

title(): -- Print title screen.
congrats(): -- Print the winning team.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from euchre.model.teams import Team

# Print the title screen for the game
def title():
    """Print the title screen for the game."""
    welcome = 'Welcome to the classic card game of Euchre!'
    
    return welcome

# Congratulate the winners of the game
def congrats(team: Team):
    """Congratulate the winners for a great game!
    
    Keyword arguments:
    team: -- the team that won the game.
    """
    if not team:
        return
    
    players = team.get_players()
    msg = f'Team {team.get_name()} HAS WON THE GAME! CONGRATULATIONS {players[0]} and {players[1]}!'
    
    return msg
    

def credits():
    """Return message for the credits information.
    """
    credit_title = """
    Euchre game code by Austin Cronin. Copyright 2025. All rights reserved.

    For inquiries or comments visit https://github.com/tincro/euchre
    """
    return credit_title