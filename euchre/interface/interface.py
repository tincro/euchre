#!/bin/python3
"""The user interface for the app."""
import sys

from PySide6.QtCore import ( 
    Qt,    
)

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget
)

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Euchre")
        self.setMinimumHeight(480)
        self.setMinimumWidth(960)
        
        # Welcome Title
        label = QLabel("Welcome to the game of Euchre!")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

def main():
    app = QApplication(sys.argv)
    win = MainInterface()
    win.show()
    app.exec()

if __name__ == '__main__':
    main()