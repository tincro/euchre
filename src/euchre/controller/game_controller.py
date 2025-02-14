"""Module for Euchre game controller."""

class EuchreController():
    def __init__(self, game, view):
        self._game = game
        self._view = view

        self._view.new_game_start_pressed.connect(self.new_game)

    def new_game(self):
        """Start new game of play."""
        self._game.new_game()