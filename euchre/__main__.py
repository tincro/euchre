#!/usr/bin/python3
"""
This is the main game loop for the Euchre game.
"""

import euchre.bots as _bots
import euchre.core as _core
import euchre.dealers as _dealers
import euchre.inputs as _inputs
import euchre.players as _players
import euchre.scores as _scores
import euchre.teams as _teams
import euchre.titles as _titles

from euchre.cards import get_highest_rank_card
from euchre.constants import (
    MAX_CARD_HAND_LIMIT,
    PLAYER_COUNT,
    TEAM_COUNT,
)

def main():
    # Present the title of the game
    _titles.title()

    # Initialize Players
    names = _inputs.get_players(PLAYER_COUNT)
    players = _players.build_players(names)

    # Initialize Bots
    bot_list = _bots.find_bots(players)
    bots = _bots.build_bots(bot_list)
    players = _bots.replace_players_with_bots(players, bots)
    
    # Set up teams
    teams = _teams.randomize_teams(players, TEAM_COUNT)
    team_list = _teams.build_teams(teams)
    _teams.assign_player_teams(team_list)
    player_seating = _teams.seat_teams(team_list)

    # Inititialize dealer object for the game to keep track of player positions in turn order
    dealer = _dealers.Dealer(player_seating)
    player_order = dealer.get_player_order()
    _core.delay()

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
            _core.delay()
                
            # Start bidding round to determine the trump suit for this hand
            # If no player wants the revealed trump to be trump, it is hidden
            # A second round of bidding starts, and players choose trump from their
            # hand. After trump is chosen, the player to dealer's left starts 
            # the first trick
            trump = _core.bidding_round(player_order, dealer, top_card)
            _core.delay()
            if trump is None:
                trump = _core.bidding_round(player_order, dealer, top_card, False)
            _core.delay()
            if trump is None:
                print('\n')
                print(f'Second round of dealing passed.')
                print('\n')
                _core.reset_round(players, dealer)
        trump.print_trump()
        _core.delay()
        trump.get_makers()
        trump.print_makers()
        print('\n')

        # The team with the most tricks wins points for the round
        round = 0
        while round < MAX_CARD_HAND_LIMIT:
            cards_played = _core.play_cards(player_order, trump)
            _core.delay()

            # For each card played this round, it is only considered if the 
            # suit matches the first card played this round. Otherwise, the card
            # is ignored. The only exception further, is if the card is considered to be
            # matching the current Trump suit. If so, that card is considered highest 
            # ranking card played in the round. Each trump is considered in ranking this way.
            winner = get_highest_rank_card(cards_played, trump)
            _core.delay()
            _scores.score_trick(winner)
            _scores.print_trick_winner(winner)
            _scores.print_tricks(player_order, team_list)
            _core.delay()
            # set winning player as the new leader for player order
            dealer.set_leader(winner[0])
            
            round += 1

        # 3 tricks wins 1 point, all 5 tricks wins 2 points
        # If a player chooses to go alone this round and wins, 4 points awarded.
        _scores.score_round(team_list, trump)
        _scores.print_scores(team_list)
        
        game_over = _scores.check_for_winner(team_list)

        if not game_over:
            # Clean up for next round
            _core.reset_round(player_order, dealer)

    # The first team to reach 10 points wins the game
    if game_over is not False:
        _titles.congrats(game_over)

# Run main game loop
if __name__ == "__main__":
    main()
