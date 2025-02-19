"""Module for Euchre game controller."""

class EuchreController():
    def __init__(self, game, view):
        self._game = game
        self._view = view

        self._view.new_game_start_pressed.connect(self.new_game)
        self.update_display(self._game.state)

    def new_game(self):
        """Start new game of play."""
        self._game.new_game()
        # for player in self._game.player_seating:
        #     self._view.create_playerLayout(player)
        self._view.create_playerLayout(self._game.player)
        self.update_display(self._game.state)

    def deal_cards(self):
        """Deal some cards."""
        self._game.dealing()
        self.update_display(self._game.state)

    def update_display(self, state):
        """Update the display."""
        match state:
            case "main_menu":
                self._view.state_main_menu()

            case "new_game":
                self._view.state_new_game()

            case "dealing":
                self._view.state_dealing()
            
            case "bidding":
                self._view.state_bidding()
            
            case "playing":
                self._view.state_playing()

            case "scoring":
                self._view.state_scoring()

            case "end_game":
                self._view.state_end_game()

            case _:
                print("BROKEN DISPLAY UPDATE.")