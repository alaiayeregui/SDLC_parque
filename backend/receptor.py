import json
import random
import numpy as np
import paho.mqtt.client as mqtt
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision

# CONFIGURACIÓN
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "rollercoaster/sensors"

INFLUX_URL = "https://eu-central-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "583Jsg7BKx38HCdEUhgK0iBygkwq_1bg5UVSEjLBEeCwf_X4JCdx7BKx_br0AlUOgF_6eqbHbEEbBkeK0LeEfw=="
INFLUX_ORG = "deusto"
INFLUX_BUCKET = "Montaña_Rusa"

SENSOR_ID = "sensor_1"

# MQTT
cliente_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# INFLUXDB
influx_client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = influx_client.write_api()

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

# ALERTAS
def comprobar_alertas(data):
    alertas = []

    acc = data["aceleracion"]
    vib = data["vibracion"]
    temp = data["temperatura"]

    if acc > 55:
        alertas.append(("CRITICAL", "ACELERACION", acc))
    elif acc > 40:
        alertas.append(("WARNING", "ACELERACION", acc))

    if vib > 60:
        alertas.append(("CRITICAL", "VIBRACION", vib))
    elif vib > 45:
        alertas.append(("WARNING", "VIBRACION", vib))

    if temp > 80:
        alertas.append(("CRITICAL", "TEMPERATURA", temp))
    elif temp > 65:
        alertas.append(("WARNING", "TEMPERATURA", temp))

    return alertas

# GUARDAR EN INFLUXDB
def guardar_influx(sensor_id, data, alertas):
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
        bucket=INFLUX_BUCKET,
        org=INFLUX_ORG,
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

        # 2. COMPROBAR ALERTAS
        alertas = comprobar_alertas(data)

        # 3. LOG ALERTAS
        if alertas:
            print("ALERTAS DETECTADAS:")
            for a in alertas:
                print(a)
        else:
            print("OK")

        # 4. GUARDAR EN INFLUXDB
        guardar_influx(sensor_id, data, alertas)

    except Exception as e:
        print("Error:", e)

# MQTT SETUP
cliente_mqtt.on_message = al_recibir

cliente_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
cliente_mqtt.subscribe("montana/sensores")

# LOOP
print("Receptor activo...")
cliente_mqtt.loop_forever()