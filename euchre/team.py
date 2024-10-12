class Team():
    """Team class is designed to keep track of information of each team."""
    def __init__(self, player_A, player_B, name):
        self._player_A = player_A
        self._player_B = player_B
        self._name = name
        self.score = 0

    def __str__(self):
        return f'Team {self._name}: {self._player_A} and {self._player_B}'
    
    def __repr__(self):
        return f'Team(\'{self._player_A}\', \'{self._player_B}\', \'{self._name}\')'

    def get_players(self):
        return [self._player_A, self._player_B]

    def get_name(self):
        return self._name

    def get_score(self):
        return self.score
    
    def set_score(self, points):
        self.score += points
