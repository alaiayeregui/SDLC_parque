import pytest
from emisor import generar_datos_sensor, generar_sensor_id

def test_generar_datos_sensor():
    datos = generar_datos_sensor()

    assert "x" in datos
    assert "y" in datos
    assert "z" in datos
    assert "temperatura" in datos

    assert -25 <= datos["x"] <= 25
    assert -20 <= datos["y"] <= 20
    assert -40 <= datos["z"] <= 10
    assert 20 <= datos["temperatura"] <= 90

def test_generar_sensor_id():
    sensor_id = generar_sensor_id()

    assert "Vagon_" in sensor_id
    assert "Eje_" in sensor_id

    partes = sensor_id.split("_")

    vagon = int(partes[1])
    eje = partes[3]

    assert 1 <= vagon <= 4
    assert eje in ["delantero", "trasero"]