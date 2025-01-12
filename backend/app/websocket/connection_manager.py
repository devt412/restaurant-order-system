from typing import List
import json
from fastapi import WebSocket
from app.core.json_utils import DateTimeEncoder


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        dead_connections = []
        json_str = json.dumps(message, cls=DateTimeEncoder)

        for connection in self.active_connections:
            try:
                await connection.send_text(json_str)
            except RuntimeError:
                dead_connections.append(connection)
            except Exception as e:
                print(f"Error sending message: {e}")
                dead_connections.append(connection)

        # Clean up dead connections
        for dead in dead_connections:
            self.disconnect(dead)


manager = ConnectionManager()
