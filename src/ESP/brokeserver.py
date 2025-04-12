import asyncio
import websockets

async def handler(websocket, path):
    print(f"Client connected on path: {path}")
    async for message in websocket:
        print("Received:", message)
        await websocket.send("Echo: " + message)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8080):
        print("WebSocket server running on ws://0.0.0.0:8080/")
        await asyncio.Future()

asyncio.run(main())
