#!/usr/bin/python3
"""This is the main game loop for the Euchre game."""

from random import sample

import inputs as _inputs
import player as _player
import scores as _scores
import team as _team
import titles as _titles
import trump as _trump
from card import Card

from constants import (
    MAX_CARD_HAND_LIMIT,
    PLAYER_COUNT,
    POINTS_TO_WIN,
    SUITS,
    TEAM_COUNT,
    VALUES,
)

DECK = [
    Card(value, suit) for value in VALUES for suit in SUITS
]
# TODO add Trump ranking for card suits
# TODO add left bower in filters for suit lead as trump
# TODO add Left Bower to show in Trump values for trump ranking
# TODO implement trump.makers to keep track of who called trump
# TODO implement trump.leftBower to keep track of left Jack
# TODO implement going alone when calling trump
# TODO filter high ranking cards if trump is played, only consider trumps
# TODO if makers win majority they win 2 points
# TODO add seating for players
# TODO add dealer functionality
# TODO add winner for hand be new hand leader
# TODO alone functionality on bidding round
# TODO refactor get_order() and get_call() to player methods
# TODO refactor main.py to make new trump instance instead of static
# TODO implement card listing to get suit as valid input for calling trump
def main():
    """Main game loop."""
    _titles.title()
    # Initialize Players
    names = _inputs.get_players(PLAYER_COUNT)
    players = _player.build_players(names)
    
    # Set up teams
    teams = _team.randomize_teams(players, TEAM_COUNT)
    team_list = _team.build_teams(teams)
    _team.assign_players(team_list)

    # Run main game loop until a Team has 10 points
    game_over = False
    while game_over is False:
        # Initialize a placeholder for Trump object
        trump = None

        # Make sure that we get a trump out of the bidding round
        # Otherwise, deal again.
        while trump is None:
            # Deal 5 cards to each player and return the top card of the leftover 
            # stack of cards (the kitty in Euchre lingo)
            top_card = deal_cards(players)
                
            # Start bidding round to determine the trump suit for this hand
            # If no player wants the revealed trump to be trump, it is hidden
            # A second round of bidding starts, and players choose trump from their
            # hand. After trump is chosen, the player to dealer's left starts 
            # the first trick
            trump = bidding_round(players, top_card)
            if trump is None:
                trump = bidding_round(players, None, top_card)
            _trump.print_trump(trump)

        # The team with the most tricks wins points for the round
        # List of cards chosen by each player to play this round.
        round = 0
        while round < MAX_CARD_HAND_LIMIT:
            cards_played = play_cards(players, trump)

            # For each card played this round, it is only considered if the 
            # suit matches the first card played this round. Otherwise, the card
            # is ignored. The only exception further, is if the card is considered to be
            # matching the current Trump suit. If so, that card is considered highest 
            # ranking card played in the round. Each trump is considered in ranking this way.
            winner = get_highest_rank_card(cards_played, trump)
            _scores.score_trick(winner)
            _scores.print_trick_winner(winner)
            _scores.print_tricks(players, team_list)
            
            round += 1

        # 3 tricks wins 1 point, all 5 tricks wins 2 points
        # If a player chooses to go alone this round and wins, 4 points awarded.
        _scores.score_round(team_list)
        _scores.print_scores(team_list)
        
        game_over = check_for_winner(team_list)

        # Clean up for next round
        reset_round(players)

    # The first team to reach 10 points wins the game
    if game_over is not False:
        _titles.congrats(game_over)



def deal_cards(players):
    """Shuffles the deck and deals cards to players in two rounds. 3 cards
    in the first round, and 2 in the second round. Returns the top 
    card left in the remaining deck.
    """
    print('\n')
    print("Dealing Cards...")
    shuffled = sample(DECK, len(DECK))
    rounds = 0
    cards_to_deal = 3
    
    while rounds < 2:
        for player in players:
            cards_dealt = shuffled [0:cards_to_deal]
            
            for card in cards_dealt:
                shuffled.remove(card)
                player.receive_card(card)
                    
        rounds += 1
        cards_to_deal -= 1

    revealed = shuffled[0]
    print(f'Revealed card to bid for trump: {revealed}')
    return revealed

def bidding_round(players, revealed=None, previous=None):
    """Bidding round for trump card for this round. If revealed is None,
    Players can choose trump from their hand.
    """
    if revealed is not None:
        for player in players:
            player.get_player_status()
            order = _inputs.get_order(revealed)
            if order == 'order':
                trump = _trump.Trump(revealed.get_suit(), player.get_team())
                return trump
            elif order == 'pass':
                continue
            else:
                print('ERROR - NOT VALID OPTION.')
    else:
        if previous is not None:
            for player in players:
                player.get_player_status()
                call = _inputs.get_call(previous)
                if call == 'pass':
                    continue
                if call:
                    trump = _trump.Trump(suit=call)
                    return trump
        else:
            print("ERROR - NO PREVIOUS CARD REFERENCED.")
    return None            

def play_cards(players, trump):
    """Each player will play a card from their hand. The card will be 
    removed from the respective players hand. Returns tuple list of (player, card played).
    """
    cards_played = []
    for player in players:
        # If a card has been played, we need to filter cards that are legal and
        # is matching the first card's suit in the list
        if len(cards_played) >= 1:
            card_to_match = cards_played[0][1]
            # Filter list of cards in player hand that is legal to play
            # If filtered list returns empty, any card in hand is legal to play
            legal_cards = player.list_cards(player.filter_cards(card_to_match, trump))
            if len(legal_cards) == 0:
                legal_cards = player.list_cards()
        else:
            legal_cards = player.list_cards()
        player.get_player_status(legal_cards, trump)            

        # Subtract 1 from player choice to index properly
        card = (_inputs.get_player_card(legal_cards) - 1)
        card_hand = legal_cards
        # Get the card from the tuple of the enumerated list
        card_to_play = card_hand[card][1]

        print(f'{player.get_name()} played {card_to_play}.')
        player.play(card_to_play)
        cards_played.append((player, card_to_play))
        
    return cards_played

def get_highest_rank_card(cards, trump):
    """Return the highest ranking card in the list by value. Returns as tuple (player, card)."""
    if not cards:
        print("ERROR - NO CARD TO EVALUATE.")
        return
    # intitialize with first card in tuple list (player, card)
    highest_card = cards[0][1]
    winning_card = cards[0]
    
    for this_card in cards:
        card = this_card[1]
        if card == highest_card:
            continue

        if card.is_trump(trump):
            if card.get_value() > highest_card.get_value():
                highest_card = card
                winning_card = this_card      
        
        if card.get_value() > highest_card.get_value():
            highest_card = card    
            winning_card = this_card

    return winning_card

def check_for_winner(team_list):
    """Check each Team for 10 or more points and returns Team if True."""
    for team in team_list:
        score = team.get_score()
        if score >= POINTS_TO_WIN:
            return team
        
    return False

def reset_round(players):
    """Reset Player counters for next round of play."""
    for player in players:
        player.reset()    

# Run main game loop
if __name__ == "__main__":
    main()