class School:
    """Modul für die Notenberechnung"""

    @staticmethod
    def calculate(grades, better_grade=False):
        """Berechnet die Durchschnittsnote und gibt sie gerundet zurück."""
        if not isinstance(grades, (list, tuple)) or not grades:
            return "Fehler: Ungültige Eingabe. Liste mit Noten erwartet."

        try:
            grades = [float(g) for g in grades] 
        except ValueError:
            return "Fehler: Alle Werte müssen Zahlen sein."

        if any(g < 1 or g > 6 for g in grades):  
            return "Fehler: Noten müssen zwischen 1 und 6 liegen."

        total = sum(grades)
        count = len(grades)
        average = total / count
        rounded_avg = round(average, 2)  

        # Zeugnisnote runden (1 Dezimalstelle, dann ganze Zahl)
        final_grade = round(average)

        # Checkbox "Bessere Note?" aktiv?
        if better_grade and final_grade > 1:
            final_grade -= 1  

        return {
            "Anzahl": count,
            "Summe": total,
            "Durchschnitt": rounded_avg,
            "Zeugnisnote": final_grade
        }

class SchoolGrades:
    @staticmethod
    def calculate(*args) -> dict:
        """Calculating School Grades
        
        raise ValueError when input is invalid

        output as follows:
        dict = {
            'count' = 0,
            'sum' = 0,
            'avg' = 0,
        }
        """
        return dict()
  
    @staticmethod
    def __validate(grades: list) -> list:
        """Validate input"""
        return grades

