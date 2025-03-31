import pytest
from modular_calc_jfy.modules.info import InformatikRechner, NumberType, DataType

@pytest.mark.parametrize("value, number_type, expected", [
    (1010, NumberType.BINARY, {"Binär": "1010", "Ternär": "101", "Oktal": "12", "Dezimal": 10}),
    (120, NumberType.DECIMAL, {"Binär": "1111000", "Ternär": "11110", "Oktal": "170", "Dezimal": 120}),
    (77, NumberType.OCTAL, {"Binär": "111111", "Ternär": "2100", "Oktal": "77", "Dezimal": 63}),
    (100, NumberType.TERTIARY, {"Binär": "1001", "Ternär": "100", "Oktal": "11", "Dezimal": 9}),
])
def test_convert_number(value, number_type, expected):
    result = InformatikRechner.convert_number(value, number_type)
    assert result == expected

@pytest.mark.parametrize("value, data_type, expected", [
    (16, DataType.BIT, {"Byte": 2.0}),
    (2, DataType.BYTE, {"Bit": 16}),
    (8, DataType.BIT, {"Byte": 1.0}),
    (1, DataType.BYTE, {"Bit": 8}),
])
def test_convert_data(value, data_type, expected):
    result = InformatikRechner.convert_data(value, data_type)
    assert result == expected

@pytest.mark.parametrize("value, number_type, expected", [
    ("not_a_number", NumberType.BINARY, "Fehler: Eingabe muss eine ganze Zahl sein."),
    (1010.5, NumberType.BINARY, "Fehler: Eingabe muss eine ganze Zahl sein."),
])
def test_convert_number_invalid(value, number_type, expected):
    result = InformatikRechner.convert_number(value, number_type)
    assert result == expected

@pytest.mark.parametrize("value, data_type, expected", [
    ("not_a_number", DataType.BIT, "Fehler: Eingabe muss eine Zahl sein."),
    (None, DataType.BYTE, "Fehler: Eingabe muss eine Zahl sein."),
])
def test_convert_data_invalid(value, data_type, expected):
    result = InformatikRechner.convert_data(value, data_type)
    assert result == expected
