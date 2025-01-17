#!/bin/python3
"""The user interface for the app."""
import sys

from PySide6.QtCore import ( 
    Qt,    
)

from PySide6.QtWidgets import (
    QApplication,
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
        new_btn = QPushButton("New Game")
        new_btn.clicked.connect(self.new_btn_slot)
        
        quit_btn = QPushButton("Quit Game")
        quit_btn.clicked.connect(self.quit_btn_slot)

        # Window Layout Declaration
        layout = QVBoxLayout()
        player_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        # Build Layout
        layout.addWidget(self.msg_label)
        layout.addLayout(player_layout)

        player_layout.addWidget(self.player_label)
        player_layout.addLayout(self.player_hand_layout)
        
        layout.addLayout(btn_layout)
        btn_layout.addWidget(new_btn)
        btn_layout.addWidget(quit_btn)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def new_btn_slot(self):
        self.msg_label.setText("New game starting...")

        _app.main(self)

    def quit_btn_slot(self):
        sys.exit()

    def credits_trigger(self):
        info = QMessageBox()
        info.setText(_titles.credits())
        info.setWindowTitle("Credits")
        info.exec()

    def howto_trigger(self):
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