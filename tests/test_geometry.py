import unittest
import pytest

from modular_calc_jfy.modules.geometry import Geometry, TriangleInvalidSitesError


# Triangle
@pytest.mark.parametrize("input_a,input_b,input_c,expected",
    [
        (3, 2, 4, {"area": 2.904738, "perimeter": 9}),
        (4, 6, 6, {"area": 11.314, "perimeter:": 16})
    ]
)
def test_triangle(input_a, input_b, input_c, expected):
    triangle = Geometry.triangle(input_a, input_b, input_c)

    assert pytest.approx(triangle["area"]) == expected["area"]
    assert traingle["perimeter"] == expected["perimeter"]


@pytest.mark.parametrize("input_a,input_b,input_c",
   [
       (2, 1, 1),
       (100, 50, 40),
   ]
)
def test_triangle_invalid(input_a, input_b, input_c):
    """Assert that TriangleInvalidsitesError is called"""
    with pytest.raises(TriangleInvalidSitesError) as e_info:
        Geometry.triangle(input_a, input_b, input_c)

# Circle
@pytest.mark.parametrize("input_diameter,expected",
    [
        (9, {"area": 63.617251, "perimeter": 26.274334}),
        (22.5, {"area": 397.60782, "perimeter:": 70.685835})
    ]
)
def test_circle(input_diameter, expected):
    circle = Geometry.circle(input_diameter)

    assert pytest.approx(circle["area"]) == expected["area"]
    assert pytest.approx(circle["perimeter"]) == expected["perimeter"]

# Parallelogram
@pytest.mark.parametrize("input_a,input_b,input_alpha,expected",
    [
        (1, 2, 20, {"area": 0.68404, "perimeter": 6}),
        (10, 5.45, 33.3, {"area": 29.921744, "perimeter:": 30.9})
    ]
)
def test_parallelogram(input_a, input_b, input_alpha, expected):
    para = Geometry.parallelogram(input_a, input_b, input_alpha)

    assert pytest.approx(para["area"]) == expected["area"]
    assert pytest.approx(para["perimeter"]) == expected["perimeter"]


