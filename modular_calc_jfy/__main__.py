#!/usr/bin/env python

"""
Copyright (C) 2024 
- Sarah Zimmermann
- Kenny Schilde
- Tommy Pahlitzsch
- Jan Meineke <jan.meineke@tracetronic.de>

All rights reserved.

The modification and distribution of this software is
hereby not permitted, unless otherwise communicated by the
offial publisher.

The use of this software is only permitted when distributed
by the official publisher or one of it's offical distributors.

--------------------------------------------------------------

This software is part of the modular calculator 'JustForYou',
a software project for compter students at BSZET Dresden.
"""

from PyQt6 import QtWidgets, uic
from pathlib import Path

import sys


UI_FILE = f"{Path(__file__).parent.resolve()}/window.ui"


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(None)
        uic.loadUi(UI_FILE, self)
         

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()

if __name__ == "__main__":
    main()
