import json
import random
import numpy as np
import paho.mqtt.client as mqtt
from datetime import datetime
import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision

load_dotenv()

# CONFIGURACIÓN
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883)) # El puerto debe ser un entero
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

token = os.getenv("INFLUX_TOKEN")
url = os.getenv("INFLUX_URL")
org = os.getenv("INFLUX_ORG")
bucket = os.getenv("INFLUX_BUCKET")

# MQTT
cliente_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# INFLUXDB
influx_client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = influx_client.write_api()

# COMPROBAR LA CONEXION
query_api = influx_client.query_api()
query = 'buckets()'
result = query_api.query(query)
print(result)

# CALCULOS
def calculos(data):
    # Calculo de aceleracion
    aceleracion = np.sqrt(
        data["x"]**2 +
        data["y"]**2 +
        data["z"]**2
    )

    # Calculo de vibración
    vibracion = aceleracion + random.uniform(0, 1)

    data = {
        **data,
        "aceleracion": aceleracion,
        "vibracion": vibracion
    }

    return data

# GUARDAR EN INFLUXDB
def guardar_influx(sensor_id, data):
    point = (
        Point("sensores")
        .tag("sensor_id", sensor_id)
        .field("eje_x", float(data["x"]))
        .field("eje_y", float(data["y"]))
        .field("eje_z", float(data["z"]))
        .field("aceleracion", float(data["aceleracion"]))
        .field("vibracion", float(data["vibracion"]))
        .field("temperatura", float(data["temperatura"]))
        .time(datetime.now(), WritePrecision.NS)
    )

    write_api.write(
        bucket=bucket,
        org=org,
        record=point
    )

# CALLBACK: MENSAJES
def al_recibir(client, userdata, msg):
    try:
        mensaje = json.loads(msg.payload.decode())

        sensor_id = mensaje["sensor_id"]
        data = mensaje["data"]

        print("\nDatos recibidos:", data)

        # 1. CALCULAR ACELERACIONY VIBRACION
        data = calculos(data)

        # 2. NOTIFICAR A LOS OBSERVADORES
        sujeto.notificar(sensor_id, data)

    except Exception as e:
        print("Error:", e)

# MQTT SETUP
cliente_mqtt.on_message = al_recibir

def iniciar_mqtt():
    cliente_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
    cliente_mqtt.subscribe(MQTT_TOPIC)


# OBSERVER PATTERN
class Observador:
    def actualizar(self):
        pass

class SujetoSensores:
    def __init__(self):
        self.observadores = []

    def suscribir(self, obs):
        self.observadores.append(obs)

    def notificar(self, sensor_id, data):
        for obs in self.observadores:
            obs.actualizar(sensor_id, data)

# OBSERVADORES
class ObservadorInflux(Observador):
    def actualizar(self, sensor_id, data):
        guardar_influx(sensor_id, data)

# SUJETO GLOBAL
sujeto = SujetoSensores()
sujeto.suscribir(ObservadorInflux())

# LOOP
def iniciar_receptor():
    print("Receptor activo...")
    cliente_mqtt.loop_forever()


if __name__ == "__main__":
    iniciar_mqtt()
    iniciar_receptor()