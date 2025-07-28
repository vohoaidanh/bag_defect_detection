from fastapi import APIRouter, WebSocket, Request
import asyncio

websocket_router = APIRouter()

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("WebSocket router loaded")
    app = websocket.app
    ws_manager = app.state.ws_manager
    await ws_manager.connect(websocket)
    try:
        await asyncio.Event().wait()  # giữ kết nối sống mãi
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        await ws_manager.disconnect(websocket)