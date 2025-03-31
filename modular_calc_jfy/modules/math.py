import math

class MathematischeFunktionen:
    @staticmethod
    def fakultaet(n):
        if n < 0:
            raise ValueError("Fakultät ist nur für nicht-negative Zahlen definiert.")
        return math.factorial(n)
    
    @staticmethod
    def quadratwurzel(x):
        if x < 0:
            raise ValueError("Quadratwurzel ist nur für nicht-negative Zahlen definiert.")
        return math.sqrt(x)
    
    @staticmethod
    def potenz(x, y):
        return x ** y
    
    @staticmethod
    def primzahlen_in_bereich(start, ende):
        def ist_primzahl(n):
            if n < 2:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True
        
        return [n for n in range(start, ende + 1) if ist_primzahl(n)]
    
    @staticmethod
    def dezimalbruch_umwandlung(x):
        from fractions import Fraction
        return Fraction(x).limit_denominator()

