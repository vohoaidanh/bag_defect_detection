import asyncio
import json
from fastapi import WebSocket

import base64
import cv2

def encode_image_to_base64(image_np):
    # Encode ảnh numpy sang JPEG
    _, buffer = cv2.imencode(".jpg", image_np)
    # Chuyển sang chuỗi base64
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64


class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.loop = asyncio.get_event_loop()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message):
        # Nếu message là dict → dump JSON
        if isinstance(message, dict):
            message = json.dumps(message)

        disconnected = []
        for conn in self.active_connections:
            try:
                await conn.send_text(message)
            except Exception:
                disconnected.append(conn)

        for conn in disconnected:
            await self.disconnect(conn)

    def broadcast_from_thread(self, message):
        img_base64 = encode_image_to_base64(message)
        # Cho phép gọi từ thread khác
        asyncio.run_coroutine_threadsafe(self.broadcast({
                                        "type": "image",
                                        "image": img_base64
                                    }), self.loop)
