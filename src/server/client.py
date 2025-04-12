# client.py
import asyncio
import websockets

async def hello():
    uri = "ws://169.234.106.230:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            msg = input("Send to server: ")
            await websocket.send(msg)
            response = await websocket.recv()
            print(f"Server replied: {response}")

if __name__ == "__main__":
    asyncio.run(hello())
