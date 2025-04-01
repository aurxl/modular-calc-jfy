class Kreditrechner:
    def __init__(self, kreditbetrag, zinssatz, laufzeit, ratenhoehe=None):
        self.kreditbetrag = kreditbetrag
        self.zinssatz = zinssatz / 100  # Zinssatz in Dezimalform
        self.laufzeit = laufzeit  # Monate
        self.ratenhoehe = ratenhoehe
    
    def kredit_einmalige_rueckzahlung(self):
        gesamtkosten = self.kreditbetrag * (1 + self.zinssatz * (self.laufzeit / 12))
        return gesamtkosten
    
    def kredit_mit_raten(self):
        if self.ratenhoehe:
            # Berechnung der Laufzeit basierend auf der Rate
            laufzeit = -(self.kreditbetrag * self.zinssatz / 12) / (self.ratenhoehe - (self.kreditbetrag * self.zinssatz / 12))
            return laufzeit
        else:
            # Berechnung der monatlichen Rate basierend auf der Laufzeit
            monatliche_rate = (self.kreditbetrag * (self.zinssatz / 12)) / (1 - (1 + self.zinssatz / 12) ** -self.laufzeit)
            return monatliche_rate

