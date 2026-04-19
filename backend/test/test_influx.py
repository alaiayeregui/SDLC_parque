from unittest.mock import MagicMock
from receptor import guardar_influx

def test_guardar_influx():
    mock_write_api = MagicMock()

    data = {
        "x": 1,
        "y": 2,
        "z": 3,
        "aceleracion": 4,
        "vibracion": 5,
        "temperatura": 30
    }

    # Simular sensor
    sensor_id = "Vagon_1_Eje_delantero"

    # Inyectar mock
    guardar_influx.__globals__["write_api"] = mock_write_api

    guardar_influx(sensor_id, data)

    assert mock_write_api.write.called