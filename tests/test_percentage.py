import pytest

from modular_calc_jfy.modules.percentage import Percentage

@pytest.mark.parametrize("input_value,input_percentage,expected",
    [
        (100, 0.25, 125),
        (12, 0.50, 18),
        (50, 0.12, 56),
    ]
)
def test_add_percentage(input_value, input_percentage, expected):
    assert pytest.approx(Percentage.add_percentage(input_value, input_percentage)) == expected

@pytest.mark.parametrize("input_value,input_percentage,expected",
    [
        (125, 0.81, 23.75),
        (15, 0.33, 10.05),
        (50, 0.12, 44),
    ]
)
def test_sub_percentage(input_value, input_percentage, expected):
    assert pytest.approx(Percentage.sub_percentage(input_value, input_percentage)) == expected

@pytest.mark.parametrize("input_value,input_share,expected",
    [
        (100, 0.25, 25),
        (50, 0.2, 10),
        (80, 0.625, 50),
    ]
)
def test_percentage_of(input_value, input_share, expected):
    assert pytest.approx(Percentage.percentage_of(input_value, input_share)) == expected

@pytest.mark.parametrize("input_g,input_w,expected_p",
    [
        (30, 15, 0.5),
        (50, 10, 0.2),
        (80, 4, 0.05),
    ]
)
def test_percentage(input_g, input_w, expected_p):
    assert pytest.approx(Percentage.percentage(input_g, input_w)) == expected_p

@pytest.mark.parametrize("input_net,expected",
    [
        (1000, 1190),
        (250, 297.5),
        (3.25, 3.87),
    ]
)
def test_gross(input_net,expected):
    assert pytest.approx(Percentage.gross(input_net, input_w)) == expected_p

@pytest.mark.parametrize("input_gross,expected",
    [
        (1000, 840.34),
        (250, 210.08),
        (16.5, 13.87),
    ]
)
def test_net(input_gross,expected):
    assert pytest.approx(Percentage.net(input_gross, input_w)) == expected_p

