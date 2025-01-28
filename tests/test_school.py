import pytest

from modular_calc_jfy.modules.school import SchoolGrades

@pytest.mark.parametrize("args,expected,",
    [
        ((3, 1, 4), {"count": 3, "sum": 11, "avg": 2.666665}),
        ((1, 1, 4, 5, 2), {"count": 5, "sum": 13, "avg": 2.6}),
    ]
)
def test_calculate(args, expected):
    calc = SchoolGrades.calculate(*args)

    assert pytest.approx(calc["avg"]) == expected["avg"]
    assert calc["sum"] == expected["sum"]
    assert calc["count"] == expected["count"]

@pytest.mark.parametrize("args",
    [
        ((3, 1, 4, 'a')),
        ((1, 1, 4, 5, 8)),
    ]
)
def test_calculate_invalid(args):
    with pytest.raises(ValueError):
        calc = SchoolGrades.calculate(*args)

