import math

class Geometrie:
    @staticmethod
    def dreieck_umfang(a, b, c):
        return a + b + c
    
    @staticmethod
    def dreieck_flaeche(basis, hoehe):
        return 0.5 * basis * hoehe
    
    @staticmethod
    def kreis_umfang(radius):
        return 2 * math.pi * radius
    
    @staticmethod
    def kreis_flaeche(radius):
        return math.pi * radius ** 2
    
    @staticmethod
    def parallelogramm_umfang(a, b):
        return 2 * (a + b)
    
    @staticmethod
    def parallelogramm_flaeche(basis, hoehe):
        return basis * hoehe