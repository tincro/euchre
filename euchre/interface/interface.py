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

        # Menu
        menu = self.menuBar()
        aboutMenu = menu.addMenu("About")
        about_action = aboutMenu.addAction("View Credits")
        about_action.triggered.connect(self.about_trigger)

        # Welcome Title
        label = QLabel("Welcome to the game of Euchre!")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Buttons
        new_btn = QPushButton("New Game")
        new_btn.clicked.connect(self.new_btn_slot)
        
        quit_btn = QPushButton("Quit Game")
        quit_btn.clicked.connect(self.quit_btn_slot)     

        # Window
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        layout.addWidget(label)
        layout.addLayout(btn_layout)

        btn_layout.addWidget(new_btn)
        btn_layout.addWidget(quit_btn)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def new_btn_slot(self):
        print("New game starting...")

    def quit_btn_slot(self):
        sys.exit()

    def about_trigger(self):
        print("Made by Austin Cronin")

def main():
    app = QApplication(sys.argv)
    win = MainInterface()
    win.show()
    app.exec()

if __name__ == '__main__':
    main()