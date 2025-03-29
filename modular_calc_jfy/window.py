import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtCore

from calculator import Calculator, InvalidExpressionError


# Determine correct path for dev and prod
# MEIPASS is the dir where the EXE is running
def determine_MEIPASS(path:str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path
    return base_path

UI_FILE = f"{determine_MEIPASS(Path(__file__).parent.resolve())}/window.ui"
AUX_UI_FILE = f"{determine_MEIPASS(Path(__file__).parent.resolve())}/aux_calc.ui"
PERCENTAGE_UI_FILE= f"{determine_MEIPASS(Path(__file__).parent.resolve())}/percentage_module.ui"
CREDIT_UI_FILE= f"{determine_MEIPASS(Path(__file__).parent.resolve())}/credit_module.ui"
GEOMETRY_UI_FILE= f"{determine_MEIPASS(Path(__file__).parent.resolve())}/geometry_module.ui"



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        uic.loadUi(UI_FILE, self)

        # First try to find a stacked widget named "stackedWidget" in the UI file
        self.stacked_widget = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        
        # If not found, create one and set it as the central widget
        if not self.stacked_widget:
            print("Creating stacked widget programmatically...")
            # Store the original central widget
            original_central = self.centralWidget()
            
            # Create a new stacked widget
            self.stacked_widget = QtWidgets.QStackedWidget()
            
            # If there was an original central widget, add it as the first page
            if original_central:
                self.stacked_widget.addWidget(original_central)
            
            # Set the stacked widget as the central widget
            self.setCentralWidget(self.stacked_widget)

        self.calculator = Calculator()
        self.calc_input = ""
        
        self.input_field = self.findChild(QtWidgets.QLineEdit, "calc_input")
        self.result_display = self.findChild(QtWidgets.QLabel, "calc_display")
        self.result_display.setText("")

        self.results_table = self.findChild(QtWidgets.QTableWidget, "table_calculations")
        if self.results_table.columnCount() < 4:
            self.results_table.setColumnCount(4)
            header_item = QtWidgets.QTableWidgetItem("Modul")
            self.results_table.setHorizontalHeaderItem(3, header_item)

        self.input_field.textChanged.connect(self.update_input)

        for i in range(10):
            getattr(self, f"calc_btn_{i}").clicked.connect(lambda _, x=i: self.add_to_input(str(x)))

        self.calc_btn_add.clicked.connect(lambda: self.add_to_input("+"))
        self.calc_btn_sub.clicked.connect(lambda: self.add_to_input("-"))
        self.calc_btn_mul.clicked.connect(lambda: self.add_to_input("*"))
        self.calc_btn_div.clicked.connect(lambda: self.add_to_input("/"))
        self.calc_btn_dot.clicked.connect(lambda: self.add_to_input("."))
        self.calc_btn_bracketL.clicked.connect(lambda: self.add_to_input("("))
        self.calc_btn_bracketR.clicked.connect(lambda: self.add_to_input(")"))
        self.calc_btn_eq.clicked.connect(self.calculate)
        self.calc_btn_c.clicked.connect(self.clear_input)
        self.calc_btn_save.clicked.connect(self.save_result)

        self.button_open_auxcalc.clicked.connect(self.open_aux_calc)
        self.button_percentage_module.clicked.connect(self.show_percentage_module)

    def update_input(self):
        self.calc_input = self.input_field.text()

    def add_to_input(self, value):
        self.calc_input += value
        self.input_field.setText(self.calc_input)

    def calculate(self):
        try:
            result = str(self.calculator.calc(self.calc_input))
            self.result_display.setText(result)

            self.add_to_results_table(self.calc_input, result, "Grundrechner")

            self.calc_input = result
            self.input_field.setText(self.calc_input)
        except (InvalidExpressionError, Exception):
            self.result_display.setText("Error")

    def clear_input(self):
        self.calc_input = ""
        self.input_field.setText("")
        self.result_display.setText("")

    def save_result(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.result_display.text())

    def open_aux_calc(self):
        aux_dialog = QtWidgets.QDialog(self)
        uic.loadUi(AUX_UI_FILE, aux_dialog)

        self.aux_calc_input = aux_dialog.findChild(QtWidgets.QLineEdit, "aux_calc_input")
        self.aux_calc_display = aux_dialog.findChild(QtWidgets.QLabel, "aux_calc_display")
        self.aux_calc_display.setText("")

        for i in range(10):
            getattr(aux_dialog, f"aux_calc_btn_{i}").clicked.connect(lambda _, x=i: self.aux_add_to_input(str(x)))

        aux_dialog.findChild(QtWidgets.QPushButton, "aux_calc_btn_add").clicked.connect(lambda: self.aux_add_to_input("+"))
        aux_dialog.findChild(QtWidgets.QPushButton, "aux_calc_btn_sub").clicked.connect(lambda: self.aux_add_to_input("-"))
        aux_dialog.findChild(QtWidgets.QPushButton, "aux_calc_btn_mul").clicked.connect(lambda: self.aux_add_to_input("*"))
        aux_dialog.findChild(QtWidgets.QPushButton, "aux_calc_btn_div").clicked.connect(lambda: self.aux_add_to_input("/"))
        aux_dialog.findChild(QtWidgets.QPushButton, "aux_calc_btn_bracketL").clicked.connect(lambda: self.aux_add_to_input("("))
        aux_dialog.findChild(QtWidgets.QPushButton, "aux_calc_btn_bracketR").clicked.connect(lambda: self.aux_add_to_input(")"))
        aux_dialog.findChild(QtWidgets.QPushButton, "aux_calc_btn_dot").clicked.connect(lambda: self.aux_add_to_input("."))
        aux_dialog.findChild(QtWidgets.QPushButton, "aux_calc_btn_eq").clicked.connect(self.aux_calculate)
        aux_dialog.findChild(QtWidgets.QPushButton, "aux_calc_btn_c").clicked.connect(self.aux_clear_input)
        aux_dialog.findChild(QtWidgets.QPushButton, "aux_calc_btn_save").clicked.connect(self.aux_save_result)

        aux_dialog.findChild(QtWidgets.QPushButton, "aux_btn_close").clicked.connect(aux_dialog.close)
        aux_dialog.exec()

    def aux_add_to_input(self, value):
        self.aux_calc_input.setText(self.aux_calc_input.text() + value)

    def aux_calculate(self):
        try:
            result = str(self.calculator.calc(self.aux_calc_input.text()))
            self.aux_calc_display.setText(result)
            self.add_to_results_table(self.aux_calc_input.text(), result, "Hilfsrechner")
            self.aux_calc_input.setText(result)
        except (InvalidExpressionError, Exception):
            self.aux_calc_display.setText("Error")

    def aux_clear_input(self):
        self.aux_calc_input.setText("")
        self.aux_calc_display.setText("")

    def aux_save_result(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.aux_calc_display.text())

    def show_main_view(self):
        # Switch back to the main calculator view (index 0)
        self.stacked_widget.setCurrentIndex(0)
        self.setWindowTitle("Rechnerprojekt - Startmodul")

    def show_percentage_module(self):
        # Create the percentage module widget
        self.percentage_ui = QtWidgets.QWidget()
        uic.loadUi(PERCENTAGE_UI_FILE, self.percentage_ui)

        # Connect the back button
        btn_back_percentage = self.percentage_ui.findChild(QtWidgets.QPushButton, "btn_back_percentage")
        if btn_back_percentage:
            btn_back_percentage.clicked.connect(self.show_main_view)

        # Check if we already have a percentage widget in the stacked widget
        percentage_widget_index = -1
        for i in range(self.stacked_widget.count()):
            if self.stacked_widget.widget(i) == self.percentage_ui:
                percentage_widget_index = i
                break
        
        # If we already have a percentage widget, remove it
        if percentage_widget_index != -1:
            old_widget = self.stacked_widget.widget(percentage_widget_index)
            self.stacked_widget.removeWidget(old_widget)
            old_widget.deleteLater()
        
        # Add the new percentage widget
        self.stacked_widget.addWidget(self.percentage_ui)
        self.stacked_widget.setCurrentWidget(self.percentage_ui)
        
        self.setWindowTitle("Rechnerprojekt - Prozentrechner")

    def show_credit_module(self):
        self.stacked_widget.setCurrentIndex(2)
        self.setWindowTitle("Rechnerprojekt - Kreditberechnung")

    def show_geometry_module(self):
        self.stacked_widget.setCurrentIndex(3)
        self.setWindowTitle("Rechnerprojekt - Geometrie")

    def add_to_results_table(self, input_value, result, module_name):
        current_date = QtCore.QDate.currentDate().toString("dd.MM.yyyy")

        row_position = 0
        self.results_table.insertRow(row_position)

        self.results_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(current_date))
        self.results_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(input_value))
        self.results_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(result))
        self.results_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(module_name))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
