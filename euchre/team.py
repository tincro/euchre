"""The Team class keeps track of information of each team."""

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

    
