import sys

# from importlib import metadata
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtCore, QtGui

from modular_calc_jfy.calculator import Calculator, InvalidExpressionError
from modular_calc_jfy.backup import Backup


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

DARK_STYLE = f"{determine_MEIPASS(Path(__file__).parent.resolve())}/styles/dark_grey.qss"
LIGHT_STYLE = f"{determine_MEIPASS(Path(__file__).parent.resolve())}/styles/light.qss"
CONSOLE_STYLE = f"{determine_MEIPASS(Path(__file__).parent.resolve())}/styles/console.qss"
PERCENTAGE_UI_FILE= f"{determine_MEIPASS(Path(__file__).parent.resolve())}/percentage_module.ui"
CREDIT_UI_FILE= f"{determine_MEIPASS(Path(__file__).parent.resolve())}/credit_module.ui"
GEOMETRY_UI_FILE= f"{determine_MEIPASS(Path(__file__).parent.resolve())}/geometry_module.ui"

VERSION = "0.1.0" # metadata.version(__package__)
COPYRIGHT = """
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
"""

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        uic.loadUi(UI_FILE, self)
        self.app = QtWidgets.QApplication.instance()
        self.theme = "System"

        self.stacked_widget = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        
        if not self.stacked_widget:
            original_central = self.centralWidget()
            
            self.stacked_widget = QtWidgets.QStackedWidget()
            
            if original_central:
                self.stacked_widget.addWidget(original_central)
            
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
        self.button_credit_module.clicked.connect(self.show_credit_module)
        self.button_geometry_module.clicked.connect(self.show_geometry_module)

        # Handling import/export of results table
        self.backuphandler = Backup(self)
        self.button_export.clicked.connect(self.backuphandler.export_data)
        self.button_import.clicked.connect(self.backuphandler.import_data)

        # Handling menubar objects
        self.action_team.triggered.connect(self.about_team)
        self.action_software.triggered.connect(self.about_software)
        self.action_copyright.triggered.connect(self.about_copyright)
        # Set themes
        self.action_system.triggered.connect(self.set_system_theme)
        self.action_dark.triggered.connect(self.theme_dark)
        self.action_light.triggered.connect(self.theme_light)
        self.action_console.triggered.connect(self.theme_console)
        # Set Font
        self.action_arial.triggered.connect(self.font_arial)
        self.action_sans_serif.triggered.connect(self.font_sans_serif)
        self.action_helvetica.triggered.connect(self.font_helvetica)
        self.action_times_new_roman.triggered.connect(self.font_times_new_roman)
        self.action_10.triggered.connect(self.font_10)
        self.action_12.triggered.connect(self.font_12)
        self.action_14.triggered.connect(self.font_14)
        self.action_16.triggered.connect(self.font_16)

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
        except (InvalidExpressionError, Exception) as e:
            self.result_display.setText(f"Error: {e}")
    
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
        self.stacked_widget.setCurrentIndex(0)
        self.setWindowTitle("Rechnerprojekt - Startmodul")

    def show_percentage_module(self):
        self.percentage_ui = QtWidgets.QWidget()
        uic.loadUi(PERCENTAGE_UI_FILE, self.percentage_ui)

        btn_back_percentage = self.percentage_ui.findChild(QtWidgets.QPushButton, "btn_back_percentage")
        if btn_back_percentage:
            btn_back_percentage.clicked.connect(self.show_main_view)

        percentage_widget_index = -1
        for i in range(self.stacked_widget.count()):
            if self.stacked_widget.widget(i) == self.percentage_ui:
                percentage_widget_index = i
                break
        
        if percentage_widget_index != -1:
            old_widget = self.stacked_widget.widget(percentage_widget_index)
            self.stacked_widget.removeWidget(old_widget)
            old_widget.deleteLater()
        
        self.stacked_widget.addWidget(self.percentage_ui)
        self.stacked_widget.setCurrentWidget(self.percentage_ui)
        
        self.setWindowTitle("Rechnerprojekt - Prozentrechner")

    def show_credit_module(self):
        self.credit_ui = QtWidgets.QWidget()
        uic.loadUi(CREDIT_UI_FILE, self.credit_ui)

        btn_back_credit = self.credit_ui.findChild(QtWidgets.QPushButton, "btn_back_credit")
        if btn_back_credit:
            btn_back_credit.clicked.connect(self.show_main_view)

        credit_widget_index = -1
        for i in range(self.stacked_widget.count()):
            if self.stacked_widget.widget(i) == self.credit_ui:
                credit_widget_index = i
                break
        
        if credit_widget_index != -1:
            old_widget = self.stacked_widget.widget(credit_widget_index)
            self.stacked_widget.removeWidget(old_widget)
            old_widget.deleteLater()
        
        self.stacked_widget.addWidget(self.credit_ui)
        self.stacked_widget.setCurrentWidget(self.credit_ui)
        
        self.setWindowTitle("Rechnerprojekt - Kreditberechnung")

    def show_geometry_module(self):
        self.geometry_ui = QtWidgets.QWidget()
        uic.loadUi(GEOMETRY_UI_FILE, self.geometry_ui)

        btn_back_geometry = self.geometry_ui.findChild(QtWidgets.QPushButton, "btn_back_geometry")
        if btn_back_geometry:
            btn_back_geometry.clicked.connect(self.show_main_view)

        geometry_widget_index = -1
        for i in range(self.stacked_widget.count()):
            if self.stacked_widget.widget(i) == self.geometry_ui:
                geometry_widget_index = i
                break
        
        if geometry_widget_index != -1:
            old_widget = self.stacked_widget.widget(geometry_widget_index)
            self.stacked_widget.removeWidget(old_widget)
            old_widget.deleteLater()
        
        self.stacked_widget.addWidget(self.geometry_ui)
        self.stacked_widget.setCurrentWidget(self.geometry_ui)
        
        self.setWindowTitle("Rechnerprojekt - Geometrie")

    def add_to_results_table(self, input_value, result, module_name):
        current_date = QtCore.QDate.currentDate().toString("dd.MM.yyyy")

        row_position = 0
        self.results_table.insertRow(row_position)

        self.results_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(current_date))
        self.results_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(input_value))
        self.results_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(result))
        self.results_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(module_name))

    def about_team(self):
        QtWidgets.QMessageBox.information(self, "Über das Team", "Sarah Zimmermann\nKenny Schilde\nTommy Pahlitzsch\nJan Meineke")

    def about_software(self):
        QtWidgets.QMessageBox.information(self, "Über die Software", f"{__package__} {VERSION}")

    def about_copyright(self):
        QtWidgets.QMessageBox.information(self, "Über das Copyright", f"{COPYRIGHT}")

    def set_theme(self, theme):
        self.theme = theme
        file = QtCore.QFile(theme)
        file.open(QtCore.QFile.OpenModeFlag.ReadOnly)
        contents = file.readAll().data().decode()
        self.app.setStyleSheet(contents)

    def set_system_theme(self):
        self.theme = "System"
        self.app.setStyleSheet(f"QWidget {{font: {self.app.font().pointSize()}pt {self.app.font().family()};}}")

    def theme_dark(self):
        self.set_theme(DARK_STYLE)
        
    def theme_light(self):
        self.set_theme(LIGHT_STYLE)

    def theme_console(self):
        self.set_theme(CONSOLE_STYLE)

    def set_font_type(self, type:str):
        contents = ""
        self.app.setFont(QtGui.QFont(type, self.app.font().pointSize()))
        
        if self.theme != "System":
            file = QtCore.QFile(self.theme)
            file.open(QtCore.QFile.OpenModeFlag.ReadOnly)
            contents = file.readAll().data().decode()

        self.app.setStyleSheet(contents + f"QWidget {{font: {self.app.font().pointSize()}pt {type};}}")

    def font_arial(self):
        self.set_font_type("Arial")

    def font_sans_serif(self):
        self.set_font_type("Sans Serif")

    def font_helvetica(self):
        self.set_font_type("Helvetica")

    def font_times_new_roman(self):
        self.set_font_type("Times New Roman")

    def set_font_size(self, size:str):
        contents = ""
        self.app.setFont(QtGui.QFont(self.app.font().family(), size))

        if self.theme != "System":
            file = QtCore.QFile(self.theme)
            file.open(QtCore.QFile.OpenModeFlag.ReadOnly)
            contents = file.readAll().data().decode()

        self.app.setStyleSheet(contents + f"QWidget {{font: {size}pt {self.app.font().family()};}}")

    def font_10(self):
        self.set_font_size(10)

    def font_12(self):
        self.set_font_size(12)

    def font_14(self):
        self.set_font_size(14)

    def font_16(self):
        self.set_font_size(16)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
