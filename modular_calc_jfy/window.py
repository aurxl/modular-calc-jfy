import sys


from pathlib import Path
from PyQt6 import QtWidgets, uic


UI_FILE = f"{Path(__file__).parent.resolve()}/window.ui"


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(None)
        uic.loadUi(UI_FILE, self)
 
