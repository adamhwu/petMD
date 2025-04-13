# server.py
import asyncio
from websockets.asyncio.server import broadcast
import websockets
import base64
import numpy as np
import cv2
import json

connected_clients = set() 

async def handler(websocket):
    connected_clients.add(websocket)
    print("Client connected")
    print(connected_clients)
    package = {}

    try:
        async for message in websocket:
            # data = json.loads(message)
            # if isinstance(data, str):
            #     data = json.loads(data)
            #
            # if data["type"] == "sensor":
            #     package = {
            #         "type": "sensor", 
            #         "temperature": data["temperature"],
            #         "humidity": data["humidity"],
            #         "pulse": data["pulse"]
            #     }
            #     json_msg = json.dumps(package)
            #
            # else:
            #     json_msg = json.dumps(data)
            #
            broadcast(connected_clients, message)

    except websockets.ConnectionClosed:
        print("Client disconnected")

    finally:
        connected_clients.remove(websocket)


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
