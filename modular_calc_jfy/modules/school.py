class SchoolGrades:
    @staticmethod
    def calculate(*args) -> dict:
        """Berechnet die Noten und gibt sie als Dictionary zurück."""
        if not args:
            raise ValueError("Es wurden keine Noten übergeben.")
        
        grades = list(args)

        # Überprüfung, ob alle Werte Zahlen sind
        try:
            grades = [float(g) for g in grades]
        except ValueError:
            raise ValueError("Alle Werte müssen Zahlen sein.")

        # Überprüfung der Noten auf Gültigkeit (zwischen 1 und 6)
        if any(g < 1 or g > 6 for g in grades):
            raise ValueError("Noten müssen zwischen 1 und 6 liegen.")

        total = sum(grades)
        count = len(grades)
        average = total / count
        rounded_avg = round(average, 6)  # Genauigkeit auf 6 Dezimalstellen, wie im Test erwartet

        return {
            "count": count,
            "sum": total,
            "avg": rounded_avg
        }

    @staticmethod
    def __validate(grades: list) -> list:
        """Validierung der Noten (optional für zusätzliche Checks)."""
        return grades
