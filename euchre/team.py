class Team():
    """Team class is designed to keep track of information of each team."""
    def __init__(self, player_A, player_B):
        self.player_A = player_A
        self.player_B = player_B
        self.score = 0

    def get_score(self):
        return self.score
    
    def set_score(self, points):
        self.score += points
