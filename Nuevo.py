import asyncio
import BAC0
import json

async def main():

    # Cantidad de decimales por instancia
    config = {
        1: 0,  # AI1 sin decimales
        2: 1,  # AI2 con 1 decimal
        4: 0,  # AI4 sin decimales
        5: 1,  # AI5 con 1 decimal
        6: 2,  # AI6 con 2 decimales
        7: 0,  # AI7 sin decimales
        8: 1   # AI8 con 1 decimal
    }

    async with BAC0.start(ip="192.168.1.5/24") as bacnet:

        rpm = {
            "address": "192.168.1.121",
            "objects": {
                "analogInput:1": ["objectName", "presentValue"],
                "analogInput:2": ["objectName", "presentValue"],
                "analogInput:4": ["objectName", "presentValue"],
                "analogInput:5": ["objectName", "presentValue"],
                "analogInput:6": ["objectName", "presentValue"],
                "analogInput:7": ["objectName", "presentValue"],
                "analogInput:8": ["objectName", "presentValue"]
            }
        }

        while True:

            try:

                values = await bacnet.readMultiple(
                    "192.168.1.121",
                    request_dict=rpm
                )

                data = {}

                for objeto, propiedades in values.items():

                    instancia = int(objeto.split(":")[1])

                    valor = propiedades["presentValue"]

                    decimales = config.get(instancia, 2)

                    data[propiedades["objectName"]] = (
                        f"{float(valor):.{decimales}f}"
                    )

                print(json.dumps(data, indent=2, ensure_ascii=False))

            except Exception as e:

                print(f"Error: {e}")

            await asyncio.sleep(5)

asyncio.run(main())
