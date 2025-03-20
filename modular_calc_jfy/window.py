import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QClipboard

UI_FILE = f"{Path(__file__).parent.resolve()}/window.ui"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        uic.loadUi(UI_FILE, self)
        
        self.calc_input = ""
        self.input_field = self.findChild(QtWidgets.QLineEdit, "calc_input")
        self.result_display = self.findChild(QtWidgets.QLabel, "calc_display")
        self.result_display.setText("")
        
        self.input_field.textChanged.connect(self.update_input)
        
        # Connect number buttons
        for i in range(10):
            getattr(self, f"calc_btn_{i}").clicked.connect(lambda _, x=i: self.add_to_input(str(x)))
        
        # Connect operation buttons
        self.calc_btn_add.clicked.connect(lambda: self.add_to_input("+"))
        self.calc_btn_sub.clicked.connect(lambda: self.add_to_input("-"))
        self.calc_btn_mul.clicked.connect(lambda: self.add_to_input("*"))
        self.calc_btn_div.clicked.connect(lambda: self.add_to_input("/"))
        self.calc_btn_eq.clicked.connect(self.calculate)
        self.calc_btn_c.clicked.connect(self.clear_input)
        self.calc_btn_save.clicked.connect(self.save_result)
        
    def update_input(self):
        self.calc_input = self.input_field.text()
    
    def add_to_input(self, value):
        self.calc_input += value
        self.input_field.setText(self.calc_input)
    
    def calculate(self):
        try:
            result = str(eval(self.calc_input))
            self.result_display.setText(result)
            self.calc_input = result
            self.input_field.setText(self.calc_input)
        except Exception:
            self.result_display.setText("Error")
    
    def clear_input(self):
        self.calc_input = ""
        self.input_field.setText("")
        self.result_display.setText("")
    
    def save_result(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.result_display.text())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
