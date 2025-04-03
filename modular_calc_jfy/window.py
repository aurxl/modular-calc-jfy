import sys
import os

from enum import Enum
from pathlib import Path
from PyQt6 import QtWidgets, uic, QtCore, QtGui
import yaml

from modular_calc_jfy.calculator import Calculator, InvalidExpressionError
from modular_calc_jfy.backup import Backup
from modular_calc_jfy.modules.school import SchoolGrades
from modular_calc_jfy.modules.info import InformatikRechner, NumberType, DataType

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
INFO_UI_FILE= f"{determine_MEIPASS(Path(__file__).parent.resolve())}/info_module.ui"
CREDIT_UI_FILE= f"{determine_MEIPASS(Path(__file__).parent.resolve())}/credit_module.ui"
GEOMETRY_UI_FILE= f"{determine_MEIPASS(Path(__file__).parent.resolve())}/geometry_module.ui"
SCHOOL_UI_FILE= f"{determine_MEIPASS(Path(__file__).parent.resolve())}/school_module.ui"

try:
    sys._MEIPASS
    CONFIG = f"{determine_MEIPASS(Path(__file__).parent.resolve())}/modules.yaml"
    DARK_STYLE = f"{determine_MEIPASS(Path(__file__).parent.resolve())}/styles/dark_grey.qss"
    LIGHT_STYLE = f"{determine_MEIPASS(Path(__file__).parent.resolve())}/styles/light.qss"
    FANCY_STYLE = f"{determine_MEIPASS(Path(__file__).parent.resolve())}/styles/fancy.qss"
except:
    CONFIG = f"{Path(__file__).parent.resolve()}/../modules.yaml"
    DARK_STYLE = f"{Path(__file__).parent.resolve()}/../styles/dark_grey.qss"
    LIGHT_STYLE = f"{Path(__file__).parent.resolve()}/../styles/light.qss"
    FANCY_STYLE = f"{Path(__file__).parent.resolve()}/../styles/fancy.qss"

with open(CONFIG, "r") as config_file:
    config_data = yaml.safe_load(config_file)
    enabled_modules = config_data.get("modules", [])

VERSION = "1.0.0"


class Modules(Enum):
    CALCULATOR = "calculator"
    INFO = "info"
    PERCENTAGE = "percentage"
    SCHOOL = "school"
    GEOMETRY = "geometry"
    MATH = "math"
    CREDIT = "credit"
    TRANSLATION = {
        CALCULATOR: "Grundrechner",
        PERCENTAGE: "Prozentrechnung",
        INFO: "Informationstechnik",
        SCHOOL: "Schulnotenrechner",
        GEOMETRY: "Geometrie",
        CREDIT: "Kreditrechnung",
        MATH: "Mathematik"
    }


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

class ModuleHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.stacked_widget = main_window.stacked_widget
        self.modules = {}

    def load_module(self, module_name, ui_file, setup_function):
        if module_name in self.modules:
            for field in self.modules[module_name].findChildren(QtWidgets.QLineEdit):
                field.setText("")
            self.stacked_widget.setCurrentWidget(self.modules[module_name])
            setup_function(self.modules[module_name])
            return

        module_ui = QtWidgets.QWidget()
        uic.loadUi(ui_file, module_ui)

        setup_function(module_ui)
        self.stacked_widget.addWidget(module_ui)
        self.modules[module_name] = module_ui
        self.stacked_widget.setCurrentWidget(module_ui)
        self.main_window.setWindowTitle(f"Rechnerprojekt - {Modules.TRANSLATION.value[module_name]}")
        self.main_window.current_input_field.setFocus()

class ThemeFontHandler:
    def __init__(self, app):
        self.app = app
        self.theme = "System"
        self.current_theme_file = None

    def set_theme(self, theme_file):
        """Set the application theme using a stylesheet file."""
        self.theme = theme_file
        self.current_theme_file = theme_file
        file = QtCore.QFile(theme_file)
        file.open(QtCore.QFile.OpenModeFlag.ReadOnly)
        contents = file.readAll().data().decode()
        self.app.setStyleSheet(contents)

    def set_system_theme(self):
        """Reset to the system default theme."""
        self.theme = "System"
        self.app.setStyleSheet(f"QWidget {{font: {self.app.font().pointSize()}pt {self.app.font().family()};}}")

    def set_font_type(self, font_type):
        """Set the font type for the application."""
        self.app.setFont(QtGui.QFont(font_type, self.app.font().pointSize()))
        self._apply_theme_with_font()

    def set_font_size(self, font_size):
        """Set the font size for the application."""
        self.app.setFont(QtGui.QFont(self.app.font().family(), font_size))
        self._apply_theme_with_font()

    def _apply_theme_with_font(self):
        """Reapply the current theme with updated font settings."""
        if self.theme != "System" and self.current_theme_file:
            file = QtCore.QFile(self.current_theme_file)
            file.open(QtCore.QFile.OpenModeFlag.ReadOnly)
            contents = file.readAll().data().decode()
            self.app.setStyleSheet(contents + f"QWidget {{font: {self.app.font().pointSize()}pt {self.app.font().family()};}}")
        else:
            self.set_system_theme()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        uic.loadUi(UI_FILE, self)
        self.app = QtWidgets.QApplication.instance()

        self.theme_font_handler = ThemeFontHandler(self.app)

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

        self.current_calculate = Modules.CALCULATOR
        self.current_input = self.calc_input
        self.current_input_field = self.input_field
        self.current_result = ""
        self.current_result_field = self.result_display

        self.results_table = self.findChild(QtWidgets.QTableWidget, "table_calculations")
        if self.results_table.columnCount() < 4:
            self.results_table.setColumnCount(4)
            header_item = QtWidgets.QTableWidgetItem("Modul")
            self.results_table.setHorizontalHeaderItem(3, header_item)

        self.current_input_field.textChanged.connect(self.update_input)

        for i in range(10):
            getattr(self, f"calc_btn_{i}").clicked.connect(lambda _, x=i: self.add_to_input(str(x)))

        self.calc_btn_add.clicked.connect(lambda: self.add_to_input("+"))
        self.calc_btn_sub.clicked.connect(lambda: self.add_to_input("-"))
        self.calc_btn_mul.clicked.connect(lambda: self.add_to_input("*"))
        self.calc_btn_div.clicked.connect(lambda: self.add_to_input("/"))
        self.calc_btn_dot.clicked.connect(lambda: self.add_to_input("."))
        self.calc_btn_bracketL.clicked.connect(lambda: self.add_to_input("("))
        self.calc_btn_bracketR.clicked.connect(lambda: self.add_to_input(")"))
        self.calc_btn_eq.clicked.connect(self.calc_factory)
        self.calc_btn_c.clicked.connect(self.clear_input)
        self.calc_btn_save.clicked.connect(self.save_result)

        self.button_open_auxcalc.clicked.connect(self.open_aux_calc)
        self.clip_btn.clicked.connect(self.add_clipboard_input)

        # Handling import/export of results table
        self.backuphandler = Backup(self)
        self.button_export.clicked.connect(self.backuphandler.export_data)
        self.button_import.clicked.connect(self.backuphandler.import_data)

        # Handling menubar objects
        self.action_team.triggered.connect(self.about_team)
        self.action_software.triggered.connect(self.about_software)
        self.action_copyright.triggered.connect(self.about_copyright)
        # Set themes
        self.action_system.triggered.connect(self.theme_font_handler.set_system_theme)
        self.action_dark.triggered.connect(lambda: self.theme_font_handler.set_theme(DARK_STYLE))
        self.action_light.triggered.connect(lambda: self.theme_font_handler.set_theme(LIGHT_STYLE))
        self.action_fancy.triggered.connect(lambda: self.theme_font_handler.set_theme(FANCY_STYLE))
        # Set Font
        self.action_arial.triggered.connect(lambda: self.theme_font_handler.set_font_type("Arial"))
        self.action_sans_serif.triggered.connect(lambda: self.theme_font_handler.set_font_type("Sans Serif"))
        self.action_comic_sans.triggered.connect(lambda: self.theme_font_handler.set_font_type("Comic Sans MS"))
        self.action_times_new_roman.triggered.connect(lambda: self.theme_font_handler.set_font_type("Times New Roman"))
        self.action_10.triggered.connect(lambda: self.theme_font_handler.set_font_size(10))
        self.action_12.triggered.connect(lambda: self.theme_font_handler.set_font_size(12))
        self.action_14.triggered.connect(lambda: self.theme_font_handler.set_font_size(14))
        self.action_16.triggered.connect(lambda: self.theme_font_handler.set_font_size(16))

        self.module_handler = ModuleHandler(self)

        # Fill in combo box with enabled modules
        self.combo_box_modules.addItems([Modules.TRANSLATION.value[Modules.CALCULATOR.value]] + [Modules.TRANSLATION.value[module] for module in enabled_modules])
        self.combo_box_modules.currentTextChanged.connect(self.show_module)
        self.show_module(value=Modules.TRANSLATION.value[Modules.CALCULATOR.value])

    def setup_input_fields(self, input_fields, result_field=None):
        for field in input_fields:
            field.focusInEvent = lambda _, f=field: self.set_current_input_field(f)
        self.current_input_field = input_fields[0]
        self.current_result_field = result_field
        self.current_input_field.setFocus()

    def set_current_input_field(self, object):
        if self.current_input_field != object: self.current_input = ""
        self.current_input_field = object
        self.current_input_field.textChanged.connect(self.update_input)
        self.current_input_field.returnPressed.connect(self.calc_factory)
        self.current_input_field.setFocus()

    def connect_buttons(self, button_mapping):
        for button, function in button_mapping.items():
            button.clicked.connect(function)

    def update_input(self):
        self.current_input = self.current_input_field.text()
        self.current_input_field.setFocus()

    def add_to_input(self, value):
        if self.current_calculate == Modules.SCHOOL and self.current_input != "":
            value = f",{value}"
        self.current_input += value
        self.current_input_field.setText(self.current_input)
        # self.current_input_field.setFocus()

    def calc_factory(self):
        match self.current_calculate:
            case Modules.CALCULATOR:
                self.calculate()
            case Modules.SCHOOL:
                self.school_calculate()
            case Modules.PERCENTAGE:
                self.calculate_percentage()
            case Modules.INFO:
                if self.info_ui.current_view == 0:
                    self.calculate_bit_byte()
                else:
                    self.calculate_number_systems()

    def calculate(self):
        try:
            print(1)
            if self.current_input == "":
                return
            self.calc_input = self.current_input
            result = str(round(self.calculator.calc(self.calc_input), 6))
            self.result_display.setText(result)

            self.add_to_results_table(self.calc_input, result, "Grundrechner")

            self.calc_input = None
            self.input_field.setText(self.calc_input)
        except (InvalidExpressionError, Exception) as e:
            self.result_display.setText(f"Error: {e}")

    def clear_input(self):
        self.current_input = ""
        self.current_input_field.setText("")
        if self.current_result_field:
            self.current_result_field.setText("")

    def save_result(self):
        if self.current_result_field:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(self.current_result_field.text())
    
    def add_clipboard_input(self):
        clipboard = QtWidgets.QApplication.clipboard()
        self.add_to_input(clipboard.text())

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
            result = str(round(self.calculator.calc(self.aux_calc_input.text()), 6))
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

        self.current_input = ""
        self.current_input_field = self.input_field
        self.current_input_field.returnPressed.connect(self.calc_factory)
        self.current_input_field.setFocus()
        self.current_calculate = Modules.CALCULATOR

    def setup_percentage_module(self, module_ui):
        self.percentage_ui = module_ui

        # Find UI elements
        self.combo_function = self.percentage_ui.findChild(QtWidgets.QComboBox, "combo_function")
        self.stacked_inputs = self.percentage_ui.findChild(QtWidgets.QStackedWidget, "stacked_inputs")
        self.result_value = self.percentage_ui.findChild(QtWidgets.QLabel, "result_value")

        # Connect combo box and calculate button
        self.combo_function.currentIndexChanged.connect(self.on_percentage_function_changed)
        self.connect_buttons({
            self.percentage_ui.findChild(QtWidgets.QPushButton, "btn_calculate"): self.calculate_percentage
        })

        # Set up input fields
        input_fields = [
            self.percentage_ui.findChild(QtWidgets.QLineEdit, name)
            for name in [
                "input_add_value", "input_add_percent", "input_gross_net", "input_gross_tax",
                "input_net_gross", "input_net_tax", "input_of_percent", "input_of_value",
                "input_percentage_base", "input_percentage_part", "input_sub_percent", "input_sub_value"
            ]
        ]
        self.setup_input_fields(input_fields, self.result_value)

        # Initialize display
        self.on_percentage_function_changed(0)
        self.current_calculate = Modules.PERCENTAGE

    def on_percentage_function_changed(self, index):
        """Ändert die angezeigten Eingabefelder je nach ausgewählter Funktion."""
        self.stacked_inputs.setCurrentIndex(index)
        self.result_value.setText("0.00")

        match index:
            case 0:
                self.current_input_field = self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_add_value")
            case 1:
                self.current_input_field = self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_sub_value")
            case 2:
                self.current_input_field = self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_of_value")
            case 3:
                self.current_input_field = self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_percentage_base")
            case 4:
                self.current_input_field = self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_gross_net")
            case 5:
                self.current_input_field = self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_net_gross")
            case _:
                self.current_input_field = None
        self.current_input = ""
        self.current_input_field.setFocus()

    def calculate_percentage(self):
        """Berechnet das Ergebnis basierend auf der ausgewählten Funktion und den Eingabewerten."""
        from modular_calc_jfy.modules.percentage import Percentage
        
        function_index = self.combo_function.currentIndex()
        result = 0.0
        input_text = ""
        
        try:
            # Prozent dazu
            if function_index == 0:
                value = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_add_value").text())
                percent = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_add_percent").text()) / 100
                result = Percentage.add_percentage(value, percent)
                input_text = f"{value} + {percent*100}%"
            
            # Prozent weg
            elif function_index == 1:
                value = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_sub_value").text())
                percent = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_sub_percent").text()) / 100
                result = Percentage.sub_percentage(value, percent)
                input_text = f"{value} - {percent*100}%"
            
            # Prozent davon
            elif function_index == 2:
                value = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_of_value").text())
                percent = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_of_percent").text()) / 100
                result = Percentage.percentage_of(value, percent)
                input_text = f"{percent*100}% von {value}"
            
            # Prozent-Satz
            elif function_index == 3:
                base = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_percentage_base").text())
                part = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_percentage_part").text())
                result = Percentage.percentage(base, part) * 100  # Umrechnung in Prozent
                input_text = f"{part} ist wieviel % von {base}"
            
            # Bruttopreis aus Nettopreis
            elif function_index == 4:
                net = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_gross_net").text())
                tax = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_gross_tax").text())
                result = Percentage.gross(net, tax)
                input_text = f"Brutto aus {net} (MwSt: {tax}%)"
            
            # Nettopreis aus Bruttopreis
            elif function_index == 5:
                gross = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_net_gross").text())
                tax = float(self.percentage_ui.findChild(QtWidgets.QLineEdit, "input_net_tax").text())
                result = Percentage.net(gross, tax)
                input_text = f"Netto aus {gross} (MwSt: {tax}%)"
            
            # Ergebnis anzeigen und in Tabelle speichern
            self.result_value.setText(f"{result:.2f}")
            self.add_to_results_table(input_text, f"{result:.2f}", "Prozentrechner")
            
        except ValueError:
            self.result_value.setText("Fehler: Ungültige Eingabe")
        except ZeroDivisionError:
            self.result_value.setText("Fehler: Division durch Null")
        except Exception as e:
            self.result_value.setText(f"Fehler: {str(e)}")

    def setup_credit_module(self, module_ui):
        self.credit_ui = module_ui

    def setup_geometry_module(self, module_ui):
        self.geometry_ui = module_ui

    def setup_info_module(self, module_ui):
        self.info_ui = module_ui

        self.combo_function_info = self.info_ui.findChild(QtWidgets.QComboBox, "combo_function_2")
        self.stacked_inputs_info = self.info_ui.findChild(QtWidgets.QStackedWidget, "stacked_inputs_2")

        self.combo_function_info.currentIndexChanged.connect(self.on_info_function_changed)
        self.connect_buttons({
            self.info_ui.findChild(QtWidgets.QPushButton, "btn_calculate_2"): self.calculate_number_systems,
            self.info_ui.findChild(QtWidgets.QPushButton, "btn_calculate_3"): self.calculate_bit_byte
        })

        input_fields = [
            self.info_ui.findChild(QtWidgets.QLineEdit, name)
            for name in ["input_add_value_2", "input_add_percent_2", "input_sub_value_2"]
        ]
        self.setup_input_fields(input_fields)

        self.on_info_function_changed(0)
        self.current_calculate = Modules.INFO

    def on_info_function_changed(self, index):
        """Ändert die angezeigten Eingabefelder je nach ausgewählter Funktion."""
        self.stacked_inputs_info.setCurrentIndex(index)
        self.info_ui.current_view = index
        if index == 1:
            self.current_input_field = self.info_ui.input_sub_value_2
        else:
            self.current_input_field = self.info_ui.input_add_value_2
        
        self.current_input = ""
        self.current_input_field.setFocus()

    def calculate_number_systems(self):
        """Berechnet die Umwandlung zwischen verschiedenen Zahlensystemen."""
        try:
            value = self.info_ui.findChild(QtWidgets.QLineEdit, "input_sub_value_2").text()
            
            number_type = NumberType.DECIMAL
            
            decimal_value = int(value)
            
            binary = bin(decimal_value)[2:]  # Binär
            ternary = InformatikRechner.to_base(decimal_value, 3)  # Ternär
            octal = oct(decimal_value)[2:]  # Oktal
            
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_2").setText(str(binary))
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_4").setText(str(ternary))
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_3").setText(str(octal))
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_5").setText(str(decimal_value))
            
            input_text = f"Umrechnung {value} (Basis 10)"
            result_text = f"Bin: {binary}, Ter: {ternary}, Okt: {octal}, Dez: {decimal_value}"
            self.add_to_results_table(input_text, result_text, "Informationstechnik")
            
        except ValueError:
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_2").setText("Fehler")
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_4").setText("Fehler")
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_3").setText("Fehler")
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_5").setText("Fehler")
        except Exception as e:
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_2").setText(f"Fehler: {str(e)}")
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_4").setText("Fehler")
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_3").setText("Fehler")
            self.info_ui.findChild(QtWidgets.QLabel, "result_value_5").setText("Fehler")
    
    def calculate_bit_byte(self):
        """Berechnet die Umwandlung zwischen Bit und Byte."""
        try:
            bit_input = self.info_ui.findChild(QtWidgets.QLineEdit, "input_add_value_2").text()
            byte_input = self.info_ui.findChild(QtWidgets.QLineEdit, "input_add_percent_2").text()
            
            result = {}
            input_text = ""
            
            if bit_input and not byte_input:
                result = InformatikRechner.convert_data(float(bit_input), DataType.BIT)
                input_text = f"{bit_input} Bit"
                
                self.info_ui.findChild(QtWidgets.QLineEdit, "input_add_percent_2").setText(str(result["Byte"]))
                
            elif byte_input and not bit_input:
                result = InformatikRechner.convert_data(float(byte_input), DataType.BYTE)
                input_text = f"{byte_input} Byte"
                
                self.info_ui.findChild(QtWidgets.QLineEdit, "input_add_value_2").setText(str(result["Bit"]))
            
            else:
                raise ValueError("Bitte nur ein Feld ausfüllen")
            
            result_text = f"Bit: {result.get('Bit', bit_input)}, Byte: {result.get('Byte', byte_input)}"
            self.add_to_results_table(input_text, result_text, "Informatik")
            
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Fehler", str(e))
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")

    def setup_school_module(self, module_ui):
        self.school_ui = module_ui

        self.setup_input_fields([self.school_ui.input], self.school_ui.result)
        self.current_input_field = self.school_ui.input
        self.current_input_field.setFocus()
        self.current_calculate = Modules.SCHOOL

    def school_calculate(self):
        try:
            result = SchoolGrades.calculate(self.current_input.split(","))
            self.school_ui.result.setText(f"Anzahl: {result['count']}\nSumme: {result['sum']}\nDurchschnitt: {result['avg']}")
            self.add_to_results_table(input_value=self.current_input, result=str(result), module_name="Schulnotenrechner")
        except Exception as exc:
            self.school_ui.result.setText(str(exc))
        

    def add_to_results_table(self, input_value, result, module_name):
        current_date = QtCore.QDate.currentDate().toString("dd.MM.yyyy")

        row_position = 0
        self.results_table.insertRow(row_position)

        self.results_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(current_date))
        self.results_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(input_value))
        self.results_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(result))
        self.results_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(module_name))

    def show_module(self, value:str):
        if value == Modules.TRANSLATION.value[Modules.GEOMETRY.value]:
            self.module_handler.load_module("geometry", GEOMETRY_UI_FILE, self.setup_geometry_module)
        elif value == Modules.TRANSLATION.value[Modules.INFO.value]:
            self.module_handler.load_module("info", INFO_UI_FILE, self.setup_info_module)
        elif value == Modules.TRANSLATION.value[Modules.PERCENTAGE.value]:
            self.module_handler.load_module("percentage", PERCENTAGE_UI_FILE, self.setup_percentage_module)
        elif value == Modules.TRANSLATION.value[Modules.CREDIT.value]:
            self.module_handler.load_module("credit", CREDIT_UI_FILE, self.setup_credit_module)
        elif value == Modules.TRANSLATION.value[Modules.SCHOOL.value]:
            self.module_handler.load_module("school", SCHOOL_UI_FILE, self.setup_school_module)
            # self.current_input_field.textChanged.connect(self.update_input)
        elif value == Modules.TRANSLATION.value[Modules.MATH.value]:
            pass
        else:
            self.show_main_view()
            self.current_input_field.textChanged.connect(self.update_input)

        self.current_input = ""
        self.current_input_field.setFocus()

    def about_team(self):
        QtWidgets.QMessageBox.information(self, "Über das Team", "Sarah Zimmermann\nKenny Schilde\nTommy Pahlitzsch\nJan Meineke")

    def about_software(self):
        QtWidgets.QMessageBox.information(self, "Über die Software", f"{__package__} {VERSION}")

    def about_copyright(self):
        QtWidgets.QMessageBox.information(self, "Über das Copyright", f"{COPYRIGHT}")

if __name__ == "__main__":
    # Force the use of XCB platform plugin
    os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())