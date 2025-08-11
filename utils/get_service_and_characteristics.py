import asyncio

from bleak import BleakClient

async def main():
    from utils.scanner import find_device

    device, adv = await find_device()

    client = BleakClient(device)
    await client.connect()

    print(f"Device name: {device.name}")
    for service in client.services:
        print(f"Service: {service.description}; uuid: {service.uuid}")
        for characteristic in service.characteristics:
            print(f"    Description: {characteristic.description};"
                  f" uuid: {characteristic.uuid};"
                  f" properties: {characteristic.properties};"
                  f" descriptors: {characteristic.descriptors}")
        print()

    await asyncio.sleep(1)
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())