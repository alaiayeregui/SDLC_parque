from unittest.mock import MagicMock
import json
from receptor import al_recibir

def test_recepcion_mqtt():
    mock_msg = MagicMock()

    payload = {
        "sensor_id": "Vagon_1_Eje_delantero",
        "data": {
            "x": 1,
            "y": 2,
            "z": 3,
            "temperatura": 25
        }
    }

    mock_msg.payload.decode.return_value = json.dumps(payload)

    # Mock cliente y userdata
    cliente = MagicMock()

    # Ejecutar callback
    al_recibir(cliente, None, mock_msg)

    # Si no lanza excepción → OK
    assert True