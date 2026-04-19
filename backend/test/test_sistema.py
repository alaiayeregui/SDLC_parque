from emisor import generar_datos_sensor
from receptor import calculos

def test_flujo_completo_sistema():
    
    datos = generar_datos_sensor()
    assert "x" in datos and "y" in datos and "z" in datos

    procesado = calculos(datos)

    assert "aceleracion" in procesado
    assert "vibracion" in procesado
    assert procesado["aceleracion"] >= 0
    assert procesado["vibracion"] >= procesado["aceleracion"]
