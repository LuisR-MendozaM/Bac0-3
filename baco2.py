import asyncio
import BAC0
import json

DISPOSITIVOS = {
    "AHU_1": {
        "ip": "192.168.1.121",
        "puntos": [1, 2, 4, 5, 6]
    },
    "AHU_2": {
        "ip": "192.168.1.122",
        "puntos": [1, 3, 7]
    }
}

async def leer_dispositivo(bacnet, nombre):

    config = DISPOSITIVOS[nombre]

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

        nombre_objeto = propiedades.get(
            "objectName",
            objeto
        )

        valor = propiedades.get(
            "presentValue",
            None
        )

        datos[nombre_objeto] = valor

    return datos

async def main():

    async with BAC0.start(ip="192.168.1.5/24") as bacnet:

        while True:

            print("\nDispositivos disponibles:")
            for dispositivo in DISPOSITIVOS:
                print(f"- {dispositivo}")

            seleccion = input(
                "\nSeleccione un dispositivo: "
            ).strip()

            if seleccion not in DISPOSITIVOS:
                print("Dispositivo no encontrado")
                continue

            try:

                datos = await leer_dispositivo(
                    bacnet,
                    seleccion
                )

                print(
                    json.dumps(
                        datos,
                        indent=4
                    )
                )

            except Exception as e:
                print(f"Error: {e}")

asyncio.run(main())
