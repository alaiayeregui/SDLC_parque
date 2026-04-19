import pytest
from receptor import calculos

def test_calculos_basicos():
    data = {
        "x": 3,
        "y": 4,
        "z": 0,
        "temperatura": 30
    }

    resultado = calculos(data)

    # √(3² + 4² + 0²) = 5
    assert pytest.approx(resultado["aceleracion"], 0.1) == 5

    assert "vibracion" in resultado
    assert resultado["vibracion"] >= resultado["aceleracion"]