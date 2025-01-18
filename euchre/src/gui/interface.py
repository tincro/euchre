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

import src.gui.app as _app
import src.gui.titles as _titles

from docs.constants import APP

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Euchre")
        self.setMinimumHeight(480)
        self.setMinimumWidth(960)

        # Welcome Title
        self.msg_label = QLabel()
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        # Player Display
        self.player_label = QLabel()
        self.player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.player_hand_layout = QHBoxLayout()

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

        self.pass_btn = QPushButton("Pass")
        self.pass_btn.clicked.connect(self.pass_turn)
        self.pass_btn.hide()

        self.order_btn = QPushButton("Order")
        self.order_btn.clicked.connect(self.order)
        self.order_btn.hide()

        self.discard_btn = QPushButton("Discard")
        self.discard_btn.clicked.connect(self.discard)
        self.discard_btn.hide()

        # Window Layout Declaration
        layout = QVBoxLayout()
        player_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        # Build Layout
        layout.addWidget(self.msg_label)
        layout.addLayout(player_layout)

        player_layout.addWidget(self.player_label)
        player_layout.addLayout(self.player_hand_layout)
        
        layout.addLayout(self.btn_layout)
        self.btn_layout.addWidget(self.new_btn)
        self.btn_layout.addWidget(self.quit_btn)
        self.btn_layout.addWidget(self.pass_btn)
        self.btn_layout.addWidget(self.order_btn)
        self.btn_layout.addWidget(self.discard_btn)
        
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
        self.msg_label.setText("New game starting...")
        self.new_btn.hide()
        self.quit_btn.hide()

        _app.main(self)

    @Slot()
    def quit_game(self):
        """Exit the application."""
        sys.exit()

    @Slot()
    def pass_turn(self):
        """Slot to pass on the current bid."""
        print('Passing Button Pressed')
        return 'pass'

    @Slot()
    def order(self):
        """Slot to order the current bid."""
        print("order button pressed.")
    
    @Slot()
    def discard(self):
        """Slot to discard the selected card."""
        print("Discard Button pressed.")

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
    win = MainInterface()
    win.show()
    sys.exit(APP.exec())

if __name__ == '__main__':
    main()