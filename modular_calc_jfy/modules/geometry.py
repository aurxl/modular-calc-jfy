class TriangleInvalidSitesError(Exception):
    """Die Summe der Längen der Seiten b, c muss größer sein als die Länge der verbleibenden Seite a."""


class Geometry:
    """Geometry module

    output as follows:
    dict = {
        'area': 0,
        'perimeter': 0,
    }
    """

    @staticmethod
    def triangle(a: float=0, b: float=0, c: float=0) -> dict:
        pass

    @staticmethod
    def circle(diameter: float=0) -> dict:
        pass

    @staticmethod
    def parallelogram(a: float=0, b: float=0, angle: float=0) -> dict:
        pass

