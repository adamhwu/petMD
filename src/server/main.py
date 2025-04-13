# main.py
import asyncio
from websockets.asyncio.server import broadcast
import websockets

connected_clients = set() 

async def handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
           broadcast(connected_clients, message)

    except websockets.ConnectionClosed:
        print("Client disconnected")

    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "", 10000):
        print("WebSocket server started")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
