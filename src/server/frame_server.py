import asyncio
import websockets

connected_clients = set()
last_frame = None

async def handler(websocket):
    global last_frame
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            last_frame = message
            await asyncio.gather(*[
                client.send(last_frame)
                for client in connected_clients
                if client != websocket and client.open
            ])
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server running on ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

asyncio.run(main())
