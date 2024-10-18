"""The Team module has utilities to interact with the teams."""

from random import sample

# Base Team class
class Team():
    def __init__(self, player_A, player_B, name):
        """Initialize the Team object and assign players and a name via arugments.
        Score is default to zero.
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

    def get_players(self):
        """Return list of players assigned to the Team object."""
        return [self._player_A, self._player_B]

    def get_name(self):
        """Return the Team object name."""
        return self._name

    def get_score(self):
        """Return the current Team object score."""
        return self._score
    
    def set_score(self, points):
        """Set the Team score, adding points to the current score."""
        self._score += points

# Team builder 
def build_teams(teams_list):
    """Initilize teams with random generated player teams list."""
    print('\n')
    print(f'Assigning teams...')
    teams = []
    team_names = ["Red", "Black"]

    for team in zip(team_names, teams_list):
        new_team = Team(team[1][0],team[1][1], team[0])
        print(new_team)
        teams.append(new_team)

    return teams

# Randomizer for players to be assigned to Teams
def randomize_teams(players, count):
    """Randomize the players and put them into a team and return the list."""
    copy = players.copy()
    player_count = 2
    teams = []

    for _ in range(count):
        members = sample(copy, player_count)

        for member in members:
            copy.remove(member)

        teams.append(members)

    return teams

# Assign players to their respective teams
def assign_players(teams):
    """Assign players to their respective assigned teams."""
    for team in teams:
        for player in team.get_players():
            player.set_team(team)
