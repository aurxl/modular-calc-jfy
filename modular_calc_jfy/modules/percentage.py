class Percentage:
    """Modul für die Prozentrechnung"""

    @staticmethod
    def percentage_of(value: float, percent: float) -> float:
        """Berechnet den Prozentsatz eines Wertes."""
        return (value * percent)

    @staticmethod
    def add_percentage(value: float, percent: float) -> float:
        """Erhöht einen Wert um einen bestimmten Prozentsatz."""
        return value + (value * percent)

    @staticmethod
    def sub_percentage(value: float, percent: float) -> float:
        """Verringert einen Wert um einen bestimmten Prozentsatz."""
        return value - (value * percent)

    @staticmethod
    def percentage(value: float, percentage_value: float) -> float:
        """Berechnet den Prozentsatz eines Wertes basierend auf einem anderen Wert."""
        print(percentage_value / value)
        return (percentage_value / value)

    @staticmethod
    def percentage_value(base_value: float, percent: float) -> float:
        """Berechnet den Wert eines gegebenen Prozentsatzes vom Grundwert."""
        return (base_value * percent) / 100
