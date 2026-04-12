import random
import json
import numpy as np
import time
from datetime import datetime
import paho.mqtt.client as mqtt

# CONFIGURACIÓN
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "rollercoaster/sensors"

SENSOR_ID = "sensor_1"

# CLIENTE MQTT
cliente_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)

# SIMULADOR SENSOR
def generar_datos_sensor():
    ejes = {
        "x": random.uniform(-25, 25),
        "y": random.uniform(-20, 20),
        "z": random.uniform(-40, 10)
    }

    temperatura = random.uniform(20, 90)

    return {
        "x": ejes["x"],
        "y": ejes["y"],
        "z": ejes["z"],
        "temperatura": temperatura
    }

# ENVIAR DATOS
def enviar_datos_mqtt(datos):
    payload = {
        "sensor_id": SENSOR_ID,
        "timestamp": datetime.now().isoformat(),
        "data": datos
    }

    cliente_mqtt.publish(
        "montana/sensores",
        json.dumps(payload)
    )

# LOOP SENSOR
def iniciar_sensor():
    print("Sensor iniciado...")

    while True:
        datos = generar_datos_sensor()
        enviar_datos_mqtt(datos)

        print("Enviado:", datos)

        time.sleep(1)

if __name__ == "__main__":
    iniciar_sensor()