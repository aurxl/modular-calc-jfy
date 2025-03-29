from enum import Enum

class NumberType(Enum):
    BINARY = 2
    TERTIARY = 3
    OCTAL = 8
    DECIMAL = 10

class DataType(Enum):
    BIT = 1
    BYTE = 8

class InformatikRechner:
    """Modul für Informatik-Umrechnungen"""

    @staticmethod
    def convert_number(value, number_type: NumberType):
        """Konvertiert eine Zahl in verschiedene Zahlensysteme."""
        if not isinstance(value, int):
            return "Fehler: Eingabe muss eine ganze Zahl sein."

        decimal_value = int(str(value), number_type.value)  # Umwandlung in Dezimal

        return {
            "Binär": bin(decimal_value)[2:],
            "Ternär": InformatikRechner.to_base(decimal_value, 3),
            "Oktal": oct(decimal_value)[2:],
            "Dezimal": decimal_value
        }

    @staticmethod
    def convert_data(value, data_type: DataType):
        """Konvertiert Datengrößen zwischen Bit und Byte."""
        if not isinstance(value, (int, float)):
            return "Fehler: Eingabe muss eine Zahl sein."

        if data_type == DataType.BIT:
            return {"Byte": round(value / 8, 3)}  # 1 Byte = 8 Bit
        elif data_type == DataType.BYTE:
            return {"Bit": value * 8}
        else:
            return "Fehler: Unbekannter Datentyp."

    @staticmethod
    def to_base(value, base):
        """Hilfsfunktion zur Konvertierung in ein beliebiges Zahlensystem."""
        if value == 0:
            return "0"
        digits = []
        while value:
            digits.append(str(value % base))
            value //= base
        return "".join(digits[::-1])