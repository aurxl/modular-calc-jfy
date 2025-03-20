class Percentage:
    """Modul für die Prozentrechnung"""

    @staticmethod
    def percentage_of(value: float, percent: float) -> float:
        """Berechnet den Prozentsatz eines Wertes."""
        return (value * percent) / 100

    @staticmethod
    def add_percentage(value: float, percent: float) -> float:
        """Erhöht einen Wert um einen bestimmten Prozentsatz."""
        return value + (value * percent)

    @staticmethod
    def sub_percentage(value: float, percent: float) -> float:
        """Verringert einen Wert um einen bestimmten Prozentsatz."""
        return value * (1 - percent / 100)
    

    @staticmethod
    def percentage_of(value: float, percent: float) -> float:
        """Berechnet den Prozentsatz eines Wertes."""
        return (value * percent) / 100

    @staticmethod
    def percentage(value: float, percentage_value: float) -> float:
        """Berechnet den Prozentsatz eines Wertes basierend auf einem anderen Wert."""
        return (percentage_value / value) * 100

    @staticmethod
    def gross(net_value: float, tax_rate: float = 19) -> float:
        """Berechnet den Brutto-Wert aus dem Netto-Wert (Standard: 19% Mehrwertsteuer)."""
        return net_value * (1 + tax_rate / 100)

    @staticmethod
    def net(gross_value: float, tax_rate: float = 19) -> float:
        """Berechnet den Netto-Wert aus dem Brutto-Wert (Standard: 19% Mehrwertsteuer)."""
        return gross_value / (1 + tax_rate / 100)