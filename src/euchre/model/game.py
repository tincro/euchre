#!/usr/bin/python3
"""
This is the main game loop for the Euchre game in the GUI version.
This is the main class to control the game logic.
"""
# from __future__ import annotations
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from src.cards import Card, Trump
#     from src.dealers import Dealer
#     from src.players import Player

from docs.constants import (
    MAX_CARD_HAND_LIMIT,
    TEAM_COUNT,
)

from src.cards import Deck
import src.bots as _bots
import src.dealers as _dealers
import src.players as _players
import src.scores as _scores
import src.teams as _teams
import src.titles as _titles

# BUG high ace of lead suit is not counting in ranking, 
#       KH -> diamonds trump, AH played 4 pos

# TODO need to refactor how rounds are implemented.

class EuchreGame():

    def __init__(self):
        self._player = None
        self._players = None
        self._player_order = None
        self._team_list = None
        self._dealer = None
        self._deck = Deck()
        self._trump = None
        self._state = "new_game"
        self._game_over = False
    
    @property
    def players(self):
        """Return the players list."""
        return self._players
    
    @property
    def team_list(self):
        """Return the team list."""
        return self._team_list
    
    @property
    def dealer(self):
        """Return the current dealer."""
        return self._dealer
    
    @property
    def trump(self):
        """Return the current trump."""
        return self._trump
    
    @property
    def deck(self):
        """Return the deck of cards."""
        return self._deck
    
    @property
    def state(self):
        """Return the current state of the game."""
        return self._state
    
    @property
    def game_over(self):
        """Return the current game progress."""
        return self._game_over
    
    @property
    def player_order(self):
        """Return the current order of players."""
        return self._player_order
    
    def reset_round(self):
        """Cleanup for next round of play.
        
        Keyword arguments:
        players: -- list of players to reset.
        """
        for player in self.players:
            player.reset()

        self.deck.collect()
        self.dealer.next_dealer()
            
    # Main game loop for GUI
    def new_game(self):
        """Start a new game of Euchre."""

        # Initialize Bots
        bot_list = _bots.sample_bots()
        bots = _bots.build_bots(bot_list)
        
        # Initialize Players
        # names = _inputs.get_players(PLAYER_COUNT)
        names = ['Player_1']
        names.extend(bots)

        self.players = _players.build_players(names)
        
        # Set up teams
        teams = _teams.randomize_teams(self.players, TEAM_COUNT)
        self.team_list = _teams.build_teams(teams)
        _teams.assign_player_teams(self.team_list)
        player_seating = _teams.seat_teams(self.team_list)

        # Inititialize dealer object for the game to keep track of player positions in turn order
        self.dealer = _dealers.Dealer(player_seating)
        self.player_order = self.dealer.get_player_order()
       
    def game(self):
        # Run main game loop until a Team has 10 points
        while game_over is False:
            
            while self.trump is None:
                # Deal 5 cards to each player and return the top card of the leftover 
                # stack of cards (the kitty in Euchre lingo)
                top_card = self.dealer.deal_cards(self.deck)
                    
                # Start bidding round to determine the trump suit for this hand.
                # If no player orders the revealed card to be trump, it is turned face down.
                #
                # A second round of bidding starts, and players may choose trump from their
                # hand. After trump is chosen, the player to dealer's left starts 
                # the first trick.
                #
                # If by the end of the second round of bidding no trump is declared,
                # pass the dealer and repeat.
                self.trump = self.bidding_round(self.player_order, self.dealer, top_card)
                
                if self.trump is None:
                    self.trump = self.bidding_round(self.player_order, self.dealer, top_card, False)
                
                if self.trump is None:
                    print(f'Second round of dealing passed.')                
                    self.reset_round(self.players, self.dealer)

            self.trump.print_trump()
            self.trump.get_makers()
            self.trump.print_makers()
            
            # The team with the most tricks wins points for the round
            round = 0
            while round < MAX_CARD_HAND_LIMIT:
                cards_played = self.play_cards(self.player_order, self.trump)

                # For each card played this round, it is only considered if the 
                # suit matches the first card played this round. Otherwise, the card
                # is ignored. The only exception further, is if the card is considered to be
                # matching the current Trump suit. If so, that card is considered highest 
                # ranking card played in the round. Each trump is considered in ranking this way.
                winner = self.get_highest_rank_card(cards_played, self.trump)
                _scores.score_trick(winner)
                _scores.print_trick_winner(winner)
                _scores.print_tricks(self.player_order, self.team_list)
                # set winning player as the new leader for player order
                self.dealer.set_leader(winner[0])
                
                round += 1

            # 3 tricks wins 1 point, all 5 tricks wins 2 points
            # If a player chooses to go alone this round and wins, 4 points awarded.
            _scores.score_round(self.team_list, self.trump)
            _scores.print_scores(self.team_list)
            
            game_over = _scores.check_for_winner(self.team_list)

            # Clean up for next round
            self.reset_round(self.player_order, self.dealer)

        # The first team to reach 10 points wins the game
        if game_over:
            _titles.congrats(game_over)