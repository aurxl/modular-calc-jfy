class Percentage:
    """Modul für die Prozentrechnung"""

    @staticmethod
    def add_percentage(value: float, percent: float) -> float:
        """Erhöht einen Wert um einen bestimmten Prozentsatz."""
        return value * (1 + percent / 100)

    @staticmethod
    def sub_percentage(value: float, percent: float) -> float:
        """Verringert einen Wert um einen bestimmten Prozentsatz."""
        return value * (1 - percent / 100)
    

    @staticmethod
    def percentage_of(value: float, percent: float) -> float:
        """Berechnet den Prozentsatz eines Wertes."""
        return (value * percent) / 100

    @staticmethod
    def percentage(base_value: float, part_value: float) -> float:
        """Berechnet, wie viel Prozent part_value von base_value ist."""
        if base_value == 0:
            raise ValueError("Der Grundwert darf nicht 0 sein.")
        return (part_value / base_value) * 100

    @staticmethod
    def gross(net_value: float, tax_rate: float = 19) -> float:
        """Berechnet den Brutto-Wert aus dem Netto-Wert (Standard: 19% Mehrwertsteuer)."""
        return net_value * (1 + tax_rate / 100)

    @staticmethod
    def net(gross_value: float, tax_rate: float = 19) -> float:
        """Berechnet den Netto-Wert aus dem Brutto-Wert (Standard: 19% Mehrwertsteuer)."""
        return gross_value / (1 + tax_rate / 100)