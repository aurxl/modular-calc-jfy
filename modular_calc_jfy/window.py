import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic

UI_FILE = f"{Path(__file__).parent.resolve()}/window.ui"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        uic.loadUi(UI_FILE, self)

        self.button_0.clicked.connect(lambda: self.append_to_display("0"))
        self.button_1.clicked.connect(lambda: self.append_to_display("1"))
        self.button_2.clicked.connect(lambda: self.append_to_display("2"))
        self.button_3.clicked.connect(lambda: self.append_to_display("3"))
        self.button_4.clicked.connect(lambda: self.append_to_display("4"))
        self.button_5.clicked.connect(lambda: self.append_to_display("5"))
        self.button_6.clicked.connect(lambda: self.append_to_display("6"))
        self.button_7.clicked.connect(lambda: self.append_to_display("7"))
        self.button_8.clicked.connect(lambda: self.append_to_display("8"))
        self.button_9.clicked.connect(lambda: self.append_to_display("9"))
        self.button_plus.clicked.connect(lambda: self.append_to_display(" + "))
        self.button_minus.clicked.connect(lambda: self.append_to_display(" - "))
        self.button_multiply.clicked.connect(lambda: self.append_to_display(" * "))
        self.button_divide.clicked.connect(lambda: self.append_to_display(" / "))
        self.button_equals.clicked.connect(lambda: self.append_to_display(" = "))
        self.button_decimal.clicked.connect(lambda: self.append_to_display("."))

    def append_to_display(self, value):
        current_text = self.calculator_display.text()  
        self.calculator_display.setText(current_text + value)  

    def main():
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    MainWindow.main()
