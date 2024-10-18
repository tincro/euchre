"""Module for implementing scores for the players"""

from constants import MAX_CARD_HAND_LIMIT

def score_round(teams):
    """Score points for the round. The team with the majority of tricks wins points."""
    # Calculate how many tricks each team made between both players
    # The majority holder wins 1 point for their team
    # If the team wins all 5 tricks, they get two points
    scores = []
    for team in teams:
        tricks = 0
        for player in team.get_players():
            tricks += player.get_tricks()
        scores.append((team, tricks))
    
    majority = 3
    min_points = 0
    standard_points = 1
    double_points = 2
    max_points = 4 # TODO need to implement going alone point score

    # evaluate the winner
    for score in scores:
        points = min_points
        if score[1] >= majority:
            if score[1] == MAX_CARD_HAND_LIMIT:
                points = double_points
            else:
                points = standard_points
        else:
            points = min_points
        score[0].set_score(points)   

def print_scores(team_list):
        """Print the current scores for each Team."""
        print('\n')
        print('-' * 40)
        print('\t\tROUND SCORES: ')
        print('-' * 40)
        for team in team_list:
            print(f'{team}: {team.get_score()}')
        print('\n')


def calculate_team_tricks(teams):
    """Calulate and return the score of the tricks won this round."""
    scores = {}
    for team in teams:
        score = 0
        players = team.get_players()
        for player in players:
            score += player.get_tricks()
        scores[team.get_name()] = score
    return scores

def score_trick(winner):
    """Score the trick for this round increasing winning team trick count."""
    if not winner:
        print("ERROR - NO TRICK TO SCORE.")
        return
    # increase the trick count by one for this hand for the player
    player = winner[0]
    player.set_tricks()

def print_trick_winner(winner):
    """Inform the players who won the current hand"""
    player = winner[0]
    team = player.get_team()
    card = winner[1]
    print('\n')
    print(f'{player} won a trick for Team {team.get_name()} with the {card}!')    

def print_tricks(players, teams):
    """Print update of current tricks scored by each Team."""
    print('\n')
    print('-' * 40)
    print('\t\tTRICK SCORES: ')
    print('-' * 40)
    for player in players:
        print(f'{player.get_name()}: {player.get_tricks()}')
    print('\n')
    team_trick_scores = calculate_team_tricks(teams)
    for team,score in team_trick_scores.items():
        print(f'Team {team}: {score}')

