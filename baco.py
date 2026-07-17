import asyncio
import BAC0

DISPOSITIVOS = {
    "AHU_1": "192.168.1.121",
    "AHU_2": "192.168.1.122",
    "AHU_3": "192.168.1.123"
}

async def leer_dispositivo(bacnet, nombre_dispositivo):

    ip = DISPOSITIVOS[nombre_dispositivo]

    rpm = {
        "address": ip,
        "objects": {
            f"analogInput:{i}": ["objectName", "presentValue"]
            for i in range(1, 9)
        }
    }

    valores = await bacnet.readMultiple(rpm)

    return valores

async def main():

    async with BAC0.start(ip="192.168.1.5/24") as bacnet:

        while True:

            dispositivo = input(
                "\nSeleccione dispositivo (AHU_1, AHU_2, AHU_3): "
            )

            try:

                datos = await leer_dispositivo(
                    bacnet,
                    dispositivo
                )

                print(datos)

            except Exception as e:
                print(f"Error: {e}")

asyncio.run(main())
