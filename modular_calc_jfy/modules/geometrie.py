import math

class TriangleInvalidSitesError(Exception):
    """Die Summe der Länge der Seiten b, c muss größer sein als die Länge der verbleibenden Seite a."""


class Geometrie:
    @staticmethod
    def dreieck_umfang(a, b, c):
        try:
            assert (b + c > a) and (c + a > b) and (a + b > c)
        except:
            raise TriangleInvalidSitesError
        return a + b + c
    
    @staticmethod
    def dreieck_flaeche(basis, hoehe):
        return 0.5 * basis * hoehe
    
    @staticmethod
    def kreis_umfang(radius):
        return math.pi * radius

    @staticmethod
    def kreis_flaeche(radius):
        return math.pi*(radius/2)**2
    
    @staticmethod
    def parallelogramm_umfang(a, b):
        return 2 * (a + b)
    
    @staticmethod
    def parallelogramm_flaeche(basis, hoehe):
        return basis * hoehe
