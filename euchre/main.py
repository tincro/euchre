#!/usr/bin/python3
"""
This is the main game loop for the Euchre game.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Player
    from card import Card
    from trump import Trump
    from dealer import Dealer

import dealer as _dealer
import inputs as _inputs
import player as _player
import scores as _scores
import team as _team
import titles as _titles
import trump as _trump

from constants import (
    MAX_CARD_HAND_LIMIT,
    PLAYER_COUNT,
    TEAM_COUNT,
)
# BUG fix alone scoring - not giving 4 pnts
# BUG fix ranking of cards if they don't match lead suit
# TODO remove extra team member if going alone
# TODO refactor scores.caclulate_team_tricks to team.py
# TODO 'yes' as part of order card 
def main():
    """Main game loop."""
    # Present the title of the game
    _titles.title()

    # Initialize Players
    names = _inputs.get_players(PLAYER_COUNT)
    players = _player.build_players(names)
    
    # Set up teams
    teams = _team.randomize_teams(players, TEAM_COUNT)
    team_list = _team.build_teams(teams)
    _team.assign_player_teams(team_list)
    player_seating = _team.seat_teams(team_list)

    # Inititialize dealer object for the game to keep track of player positions in turn order
    dealer = _dealer.Dealer(player_seating)
    player_order = dealer.get_player_order()

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
            top_card = dealer.deal_cards()
                
            # Start bidding round to determine the trump suit for this hand
            # If no player wants the revealed trump to be trump, it is hidden
            # A second round of bidding starts, and players choose trump from their
            # hand. After trump is chosen, the player to dealer's left starts 
            # the first trick
            trump = bidding_round(player_order, dealer, top_card)
            if trump is None:
                trump = bidding_round(player_order, dealer, None, top_card)
            trump.print_trump()
            trump.get_makers()
            trump.print_makers()

        # The team with the most tricks wins points for the round
        round = 0
        while round < MAX_CARD_HAND_LIMIT:
            cards_played = play_cards(player_order, trump)

            # For each card played this round, it is only considered if the 
            # suit matches the first card played this round. Otherwise, the card
            # is ignored. The only exception further, is if the card is considered to be
            # matching the current Trump suit. If so, that card is considered highest 
            # ranking card played in the round. Each trump is considered in ranking this way.
            winner = get_highest_rank_card(cards_played, trump)
            _scores.score_trick(winner)
            _scores.print_trick_winner(winner)
            _scores.print_tricks(player_order, team_list)
            # set winning player as the new leader for player order
            dealer.set_leader(winner[0])
            
            round += 1

        # 3 tricks wins 1 point, all 5 tricks wins 2 points
        # If a player chooses to go alone this round and wins, 4 points awarded.
        _scores.score_round(team_list, trump)
        _scores.print_scores(team_list)
        
        game_over = _scores.check_for_winner(team_list)

        # Clean up for next round
        reset_round(player_order, dealer)

    # The first team to reach 10 points wins the game
    if game_over is not False:
        _titles.congrats(game_over)

def bidding_round(players: list[Player], dealer: Dealer, revealed: Card=None, previous:Card=None) -> Trump|None:
    """Start bidding round for trump card for this round. If revealed is None,
    Players can choose trump from their hand. Returns Trump object.

    Keyword arguments:
    players: -- list of players in this round of bidding.
    revealed: -- the revealed card to start the Trump bidding.
    previous: -- the same as revealed, except cannot be chosen as Trump this round.
    """
    if revealed is not None:
        for player in players:
            player.get_player_status()
            order = _inputs.get_order(revealed)
            if order == 'order':
                player.going_alone()
                dealer.pickup_and_discard(revealed)
                trump = _trump.Trump(revealed.get_suit(), player.get_team())
                return trump
            elif order == 'pass':
                continue
            else:
                print('ERROR - NOT VALID OPTION.')
    else:
        if previous is not None:
            print('\n')
            print(f'The dealer {dealer} turned the {previous} face-down. Starting second round of bidding...')
            for player in players:
                player.get_player_status()
                call = _inputs.get_call(previous)
                if call == 'pass':
                    continue
                if call:
                    player.going_alone()
                    trump = _trump.Trump(call, player.get_team())
                    return trump
        else:
            print("ERROR - NO PREVIOUS CARD REFERENCED.")
    return None            

def play_cards(players: list[Player], trump: Trump) -> list[tuple[Player, Card]]:
    """Each player plays a card from their hand. Returns tuple list of (player, card played).
    
    Keyword arguments:
    players: -- list of players.
    trump: -- trump for current round.
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
        card = (player.get_player_card(legal_cards) - 1)
        # card_hand = legal_cards
        # Get the card from the tuple of the enumerated list
        card_to_play = legal_cards[card][1]

        print(f'{player.get_name()} played {card_to_play}.')
        player.remove_card(card_to_play)
        cards_played.append((player, card_to_play))
        
    return cards_played

def get_highest_rank_card(cards: list[tuple[Player, Card]], trump: Trump) -> tuple[Player, Card]:
    """Score the highest ranking Card object in the card list by value. Returns as tuple (player, card).
    
    cards: -- list of tuples of (player, card).
    trump: -- current round Trump object.
    """
    if not cards:
        print("ERROR - NO CARD TO EVALUATE.")
        return
    # intitialize with first card in tuple list (player, card)
    highest_card = cards[0][1]
    winning_card = cards[0]
    
    for this_card in cards:
        card = this_card[1]
        if card == highest_card:
            # Check for Trump and continue
            card.is_trump(trump)
            continue

        if card.is_trump(trump):
            if card.get_value() > highest_card.get_value():
                highest_card = card
                winning_card = this_card      
        
        if card.get_value() > highest_card.get_value():
            highest_card = card    
            winning_card = this_card

    return winning_card

def reset_round(players: list[Player], dealer: Dealer):
    """Reset Player counters for next round of play.
    
    Keyword arguments:
    players: -- list of players to reset.
    """
    for player in players:
        player.reset()

    dealer.next_dealer()    

# Run main game loop
if __name__ == "__main__":
    main()