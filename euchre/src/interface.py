#!/bin/python3
"""The user interface for the app."""
import sys

from PySide6.QtCore import ( 
    Qt,    
)

from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QPushButton,
    QLabel,
    QMainWindow,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget
)

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Euchre")
        self.setMinimumHeight(480)
        self.setMinimumWidth(960)

        self.display_list = []

        # Menu
        menu = self.menuBar()
        aboutMenu = menu.addMenu("About")
        credits_action = aboutMenu.addAction("View Credits")
        credits_action.triggered.connect(self.credits_trigger)

        # Welcome Title
        label = QLabel("Welcome to the game of Euchre!")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Buttons
        new_btn = QPushButton("New Game")
        new_btn.clicked.connect(self.new_btn_slot)
        
        quit_btn = QPushButton("Quit Game")
        quit_btn.clicked.connect(self.quit_btn_slot)

        # Player Display
        self.player_label = QLabel("")
        self.player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Window Layout Declaration
        layout = QVBoxLayout()
        player_layout = QVBoxLayout()
        player_hand_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()

        # Build Layout
        layout.addWidget(label)
        layout.addLayout(player_layout)

        player_layout.addWidget(self.player_label)
        player_layout.addLayout(player_hand_layout)
        
        for i in range(5):
            card_label = QLabel(str(i+1))
            card_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            player_hand_layout.addWidget(card_label)

            self.display_list.append(card_label)
            

        layout.addLayout(btn_layout)
        btn_layout.addWidget(new_btn)
        btn_layout.addWidget(quit_btn)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def new_btn_slot(self):
        print("New game starting...")
        name_box = QInputDialog()
        text, ok = name_box.getText(self, "New Player", "Player name:")
        if ok and text:
            self.player_label.setText(f'Player: {text}')

    def quit_btn_slot(self):
        sys.exit()

    def credits_trigger(self):
        info = QMessageBox()
        info.setText("PyEuchre code by Austin Cronin.")
        info.setWindowTitle("Credits")
        info.exec()

def main():
    app = QApplication(sys.argv)
    win = MainInterface()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()