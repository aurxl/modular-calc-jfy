import unittest
import pytest

from modular_calc_jfy.modules.geometrie import Geometrie, TriangleInvalidSitesError

# Triangle
@pytest.mark.parametrize("input_a,input_b,input_c,expected",
    [
        (3, 2, 4, 9),
        (4, 6, 6, 16)
    ]
)
def test_triangle(input_a, input_b, input_c, expected):
    assert pytest.approx(Geometrie.dreieck_umfang(input_a, input_b, input_c)) == expected

@pytest.mark.parametrize("input_b,input_h,expected",
    [
        (3, 2, 3),
        (4, 6, 12)
    ]
)
def test_triangle_area(input_b, input_h, expected):
    assert pytest.approx(Geometrie.dreieck_flaeche(input_b, input_h)) == expected


@pytest.mark.parametrize("input_a,input_b,input_c",
   [
       (2, 1, 1),
       (100, 50, 40),
   ]
)
def test_triangle_invalid(input_a, input_b, input_c):
    """Assert that TriangleInvalidsitesError is called"""
    with pytest.raises(TriangleInvalidSitesError) as e_info:
        Geometrie.dreieck_umfang(input_a, input_b, input_c)

# Circle
@pytest.mark.parametrize("input_diameter,expected",
    [
        (9, (63.617251, 28.2743388)),
        (22.5, (397.60782, 70.685835))
    ]
)
def test_circle(input_diameter, expected):
    assert Geometrie.kreis_flaeche(input_diameter) == pytest.approx( expected[0])
    assert Geometrie.kreis_umfang(input_diameter) == pytest.approx( expected[1])

# Parallelogram
@pytest.mark.parametrize("input_a,input_b,expected",
    [
        (1, 2, 6),
        (10, 5.45, 30.9)
    ]
)
def test_parallelogram(input_a, input_b, expected):
    assert pytest.approx(Geometrie.parallelogramm_umfang(input_a, input_b)) == expected

@pytest.mark.parametrize("input_b,input_h,expected",
    [
        (1, 2, 2),
        (10, 5.45, 54.5)
    ]
)
def test_parallelogram_area(input_b, input_h, expected):
    assert pytest.approx(Geometrie.parallelogramm_flaeche(input_b, input_h)) == expected


