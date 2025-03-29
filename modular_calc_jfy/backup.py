import csv

from Crypto.Cipher import AES
from io import StringIO
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem


class CompromisedDataError(Exception):
    """Hash of imported Data mismatch"""


class Backup:
    """
    Handling external Files for import and exporting saves.
    """
    __key = b'o%70|yo>9%jS#!~}'

    def __init__(self, window:QMainWindow):
        self.window = window
        self.table = self.window.results_table

    def __encrypt_data(self, file:str, data:str):
        cipher = AES.new(self.__key, AES.MODE_OCB)
        data, tag = cipher.encrypt_and_digest(data.encode())

        with open(file, 'wb') as f:
            f.write(tag)
            f.write(cipher.nonce)
            f.write(data)

    def __decrypt_data(self, file:str):
        with open(file, "rb") as f:
            tag = f.read(16)
            nonce = f.read(15)
            data = f.read()

        cipher = AES.new(self.__key, AES.MODE_OCB, nonce=nonce)
        try:
            data = cipher.decrypt_and_verify(data, tag)
            QMessageBox.information(self.window, "Import", "Import der Daten erfolgreich.")
            return data
        except ValueError:
            raise CompromisedDataError

    def export_data(self):
        if self.table.rowCount() <= 0:
            return QMessageBox.information(self.window, "Export", "Keine Ergebnisse in der Liste.")

        file_name, _ = QFileDialog.getSaveFileName(self.window, "Save File", "jfy-export.bin", "*.bin")
        
        if not file_name: return

        string_io = StringIO()
        writer = csv.writer(string_io)

        for row in range(self.table.rowCount()):
            row_content = list()
            for item in range(0,4):
                row_content.append(self.table.item(row,item).text())
            writer.writerow(row_content)

        self.__encrypt_data(file=file_name, data=string_io.getvalue())
        return QMessageBox.information(self.window, "Export", "Export der Daten erfolgreich.")

    def import_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self.window, "Import", "", "*.bin")

        if not file_name: return

        try:
            data = self.__decrypt_data(file_name).decode()
        except CompromisedDataError:
            return QMessageBox.information(self.window, "Import Error", "Daten sind kompromitiert und können nicht importiert werden.")

        csv_data = csv.reader(StringIO(data))
        row_position = 0
        for line in csv_data:
            self.table.insertRow(0)
            for i in range(0, 4):
                widget_item = QTableWidgetItem(line[i])
                self.table.setItem(row_position, i, widget_item)
