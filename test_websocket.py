import asyncio
import websockets

async def test_ws():
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send("Hello from Python client")
            while True:
                msg = await websocket.recv()
                print("📨 Server replied:", msg)
    except Exception as e:
        print("❌ Connection failed:", e)

asyncio.run(test_ws())
