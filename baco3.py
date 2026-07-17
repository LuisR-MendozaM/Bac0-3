import asyncio
import BAC0

DISPOSITIVOS = {
    "UMA-09": {
        "ip": "192.168.1.121",
        "puntos": {
            i: {
                "decimales": 0 if i == 1
                else 1 if i == 2
                else 3 if i == 8
                else 2
            }
            for i in range(1, 9)
        }
    }
}

async def leer_dispositivo(bacnet, nombre_dispositivo):

    config = DISPOSITIVOS[nombre_dispositivo]

    rpm = {
        "address": config["ip"],
        "objects": {
            f"analogInput:{punto}": [
                "objectName",
                "presentValue"
            ]
            for punto in config["puntos"]
        }
    }

    valores = await bacnet.readMultiple(rpm)

    datos = {}

    for objeto, propiedades in valores.items():

        # Obtiene el número de instancia
        punto = int(objeto.split(",")[1])

        # Obtiene nombre y valor
        nombre_objeto = propiedades[0][1]
        valor = propiedades[1][1]

        # Obtiene configuración de decimales
        decimales = config["puntos"][punto]["decimales"]

        # Redondea
        valor = round(float(valor), decimales)

        datos[nombre_objeto] = valor

    return datos


async def main():

    async with BAC0.start(ip="192.168.1.5/24") as bacnet:

        dispositivo = "UMA-09"

        try:

            datos = await leer_dispositivo(
                bacnet,
                dispositivo
            )

            print("\nValores leídos:")
            for nombre, valor in datos.items():
                print(f"{nombre}: {valor}")

        except Exception as e:
            print(f"Error: {e}")


asyncio.run(main())
