#!/bin/python3
"""The user interface for the app."""
import sys

from PySide6.QtCore import ( 
    Qt,
    Slot,   
)

from PySide6.QtWidgets import (
    QPushButton,
    QLabel,
    QMainWindow,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget
)
# import src.euchre as _euchre
from src.game import EuchreGame
import src.titles as _titles

from docs.constants import APP

class EuchreGUI(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.setWindowTitle("Python Euchre")
        self.setMinimumHeight(480)
        self.setMinimumWidth(960)

        # Menu
        menu = self.menuBar()
        aboutMenu = menu.addMenu("About")
        howto_action = aboutMenu.addAction("How to play")
        howto_action.triggered.connect(self.howto_trigger)
        credits_action = aboutMenu.addAction("View Credits")
        credits_action.triggered.connect(self.credits_trigger)

        # Buttons
        self.new_btn = QPushButton("New Game")
        self.new_btn.clicked.connect(self.new_game)
        
        self.quit_btn = QPushButton("Quit Game")
        self.quit_btn.clicked.connect(self.quit_game)

        # Window Layout Declaration
        layout = QVBoxLayout()
        player_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        # Build Layout
   
        layout.addLayout(player_layout)
       
        layout.addLayout(self.btn_layout)
        self.btn_layout.addWidget(self.new_btn)
        self.btn_layout.addWidget(self.quit_btn)
               
        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def main_menu(self):
        """Main menu screen."""
        self.new_btn.show()
        self.quit_btn.show()
    
    @Slot()
    def new_game(self):
        """Slot to start a new game."""
        self.game.new_game()

    @Slot()
    def quit_game(self):
        """Exit the application."""
        sys.exit()

    @Slot()
    def credits_trigger(self):
        """Reveal the information for the credits for the game application."""
        info = QMessageBox()
        info.setText(_titles.credits())
        info.setWindowTitle("Credits")
        info.exec()

    @Slot()
    def howto_trigger(self):
        """Display the How to Play information."""
        info = QMessageBox()
        info.setText("How to play!")
        info.setWindowTitle("How to Play")
        info.exec()

def main():
    APP(sys.argv)
    game = EuchreGame()
    win = EuchreGUI(game)
    win.show()
    sys.exit(APP.exec())

if __name__ == '__main__':
    main()