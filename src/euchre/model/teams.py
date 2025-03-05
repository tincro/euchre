"""The Team module has utilities to interact with the teams.

Team(): the base Team class.
build_teams(): build Team objects.
randomize_teams(): return list of randomized list of players.
assign_player_teams(): assign players to Team objects.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from euchre.model.players import Player

from collections import deque
from random import sample

from euchre.constants import (
    TEAM_COUNT
)

# Base Team class
class Team():
    def __init__(self, player_A, player_B, name):
        """Initialize the Team object and assign players and a name via arugments.
        Score is default to zero.

        Properties:
            players -- Returns list of players assigned to the Team object.
            name -- Returns the Team object's name.
            score -- Returns the current score for the Team object.
        
        """
        self._player_A = player_A
        self._player_B = player_B
        self._name = name
        self._score = 0

    def __str__(self):
        """Return human-friendly Team object."""
        return f'Team {self._name}: {self._player_A} and {self._player_B}'
    
    def __repr__(self):
        """Return Team Object."""
        return f'Team(\'{self._player_A}\', \'{self._player_B}\', \'{self._name}\')'
    
    # Public methods
    @property
    def players(self):
        """Return list of players assigned to the Team object."""
        return [self._player_A, self._player_B]

    @property
    def name(self):
        """Return the Team object name."""
        return self._name

    @property
    def score(self):
        """Return the current Team object score."""
        return self._score
    
    @score.setter
    def score(self, points):
        """Set the Team score, adding points to the current score.
        
        Keyword arguments:
        points: -- number of points to increase score.
        """
        if points > 0:
            self._score += points

# Team builder 
def build_teams(teams_list: list[list[Player]]) -> list[Team]:
    """Initialize teams with random generated player teams list.
    
    Keyword arguments:
    teams_list: -- list of teams to assign players.
    """
    if not teams_list:
        return
    
    print('\n')
    msg = f'Assigning teams...'
    print(msg)
    teams = []
    team_names = ["Red", "Black"]

    for team in zip(team_names, teams_list):
        new_team = Team(team[1][0],team[1][1], team[0])
        print(new_team)
        teams.append(new_team)

    return teams

# Optional Randomizer for players to be assigned to Teams
def list_teams(players: list[Player], team_count: int=TEAM_COUNT, randomize=False) -> list[Team]:
    """Randomize the players and put them into a team and return the list.
    
    players: -- the list of players
    team_count: -- the number of teams
    """
    if not players or not team_count:
        return

    copy = players.copy()
    player_count = int(len(players) / team_count)
    teams = []

    for _ in range(team_count):
        if randomize:
            members = sample(copy, player_count)
        else:
            team = slice(player_count)
            members = copy[team]
            
        for member in members:
            copy.remove(member)

        teams.append(members)

    return teams

# Assign players to their respective teams
def assign_player_teams(teams: list[Team]):
    """Assign players to their respective assigned teams.
    
    Keyword arguments:
    teams: -- the list of teams to set each player.
    """
    for team in teams:
        for player in team.players:
            player.team = team

# Assign player order alternating between players in each team
def seat_teams(teams: list[Team]):
    """Seat players in alternating seats.
    
    Keyword arguments:
    teams: -- team list of players to alternate seating.
    """
    num_seats = 4
    # list players in order of seating
    players_list = [deque(team.players) for team in teams]
    player_order = []
    
    while len(player_order) < num_seats:
        for team in players_list:
            player = team.popleft()
            player_order.append(player)

    return player_order
