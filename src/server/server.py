# server.py
import asyncio
from websockets.asyncio.server import broadcast
import websockets
import base64
import numpy as np
import cv2

connected_clients = set() 

async def handler(websocket):
    connected_clients.add(websocket)
    print("Client connected")
    print(connected_clients)

    try:
        async for message in websocket:
            try:
                img_data = base64.b64decode(message)
                np_arr = np.frombuffer(img_data, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                broadcast(connected_clients, message)

            except Exception as e:
                print(f"Error: {e}")

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
