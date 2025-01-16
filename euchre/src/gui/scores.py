"""Module for implementing scores for the players.

is_euchred(): Checks if the maker team lost the majority tricks this round
check_alone(): checks if one of the players went alone this round.
score_round(): Score points for the round.
print_scores(): Print the current scores for each team.
calculate_team_tricks(): Calculate the tricks for each player.
score_trick(): Score trick of the highest ranking card.
print_trick_winner(): Print the winner of the current hand.
print_tricks(): Print scores of tricks won by each team.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.gui.cards import Card
    from src.gui.players import Player
    from src.gui.teams import Team
    from src.gui.trumps import Trump
    
from docs.constants import (
    ALONE_POINTS,
    MIN_TRICKS,
    MAX_TRICKS,
    MAJORITY_POINTS,
    MARCH_POINTS,
    POINTS_TO_WIN,
)
def is_euchred(makers: Team, winner: Team) -> bool:
    """Return True if the makers did not make the points this round.

    Keyword arguments:
    makers: Team that decided on trump this round.
    winner: Team that won the majority this round.
    """
    if makers != winner:
        return True
    return False

def check_alone(team_list: list[Team]) -> tuple[Team, True]|False:
    """Check if one of the players on the Team went alone when ordering Trump.
    
    Keyworld arguments:
    team_list: list of teams to check each Player is alone this round. Returns (Team, True) if True.
    """
    for team in team_list:
        players = team.get_players()
        for player in players:
            if player.is_alone():
                return (team, True)
            
    return False

def score_round(teams: list[Team], trump: Trump):
    """Score points for the round. The team with the majority of tricks wins points.
    
    Keyword arguments:
    teams: -- the list of teams to score points for the round.
    trump: -- the trump object for the round.
    """
    if not teams or not trump:
        return

    # Calculate how many tricks each team made between both players
    # The majority holder wins 1 point for their team
    # If the team wins all 5 tricks, they get two points
    # If a player on the winning team went alone, they get 4 points
    
    makers = trump.get_makers()
    scores = calculate_team_tricks(teams)
    is_alone = check_alone(teams)
    winner = None
    points = 0

    for team in teams:
        tricks = scores[team.get_name()]
        if tricks >= MIN_TRICKS and tricks < MAX_TRICKS:
            winner = team
            # check if the makers team got euchred this round, if so award 2 points
            if is_euchred(makers,winner):
                points = MARCH_POINTS
            else:
                # give 1 point
                points = MAJORITY_POINTS
        elif tricks == MAX_TRICKS:
            winner = team
            # is winning player went alone, give 4 points instead
            if is_alone:
                if winner == is_alone[0]:
                    points = ALONE_POINTS
            else:
                # give 2 points
                points = MARCH_POINTS

    if winner:
        winner.set_score(points)
    

def print_scores(team_list: list[Team]):
        """Print the current scores for each Team.
        
        Keyword arguments:
        team_list: -- the list of team members to print the score for the round.
        """
        if not team_list:
            return
        
        print('\n')
        print('-' * 40)
        print('\t\tROUND SCORES: ')
        print('-' * 40)
        for team in team_list:
            print(f'{team}: {team.get_score()}')
        print('\n')


def calculate_team_tricks(teams: list[Team]) -> dict[str, int]:
    """Calulate and return the score of the tricks won this round.
    
    Keyword arguments:
    teams: -- the list of teams to calculate each players tricks for the round.
    """
    if not teams:
        return
    
    scores = {}
    for team in teams:
        score = 0
        players = team.get_players()
        for player in players:
            score += player.get_tricks()
        scores[team.get_name()] = score
    return scores

def score_trick(winner: tuple[Player, Card]):
    """Score the trick for this round increasing winning team trick count.
    
    Keyword arguments:
    winner: -- tuple of the highest ranking card for the round.
    """
    if not winner:
        print("ERROR - NO TRICK TO SCORE.")
        return
    # increase the trick count by one for this hand for the player
    player = winner[0]
    player.set_tricks()

def print_trick_winner(winner: tuple[Player, Card]):
    """Inform the players who won the current hand.

    Keyword arguments:
    winner: -- tuple of the highest ranking card for the round.
    """
    if not winner:
        return
    
    player = winner[0]
    team = player.get_team()
    card = winner[1]
    print('\n')
    print(f'{player} won a trick for Team {team.get_name()} with the {card}!')    

def print_tricks(players: list[Player], teams: list[Team]):
    """Print update of current tricks scored by each Team.
    
    Keyword arguments:
    players: -- the list of players
    teams: -- the list of teams to calculate scores
    """
    if not players or not teams:
        return
    
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

def check_for_winner(team_list: list[Team]) -> Team|False:
    """Check each Team for 10 or more points. Returns Team object if True.
    
    Keyword arguments:
    team_list: -- List of Team objects to count score.
    """
    if not team_list:
        return
    
    for team in team_list:
        score = team.get_score()
        if score >= POINTS_TO_WIN:
            return team
        
    return False
