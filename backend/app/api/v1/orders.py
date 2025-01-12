from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.services.order import OrderService
from app.websocket.connection_manager import manager
from fastapi import WebSocket
from app.core.json_utils import DateTimeEncoder

router = APIRouter()
order_service = OrderService()


async def get_token(websocket: WebSocket):
    return True


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, authenticated: bool = Depends(get_token)
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle received data if needed
            await websocket.send_json({"status": "received"})
    except:
        manager.disconnect(websocket)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    new_order = order_service.create_order(order)
    await manager.broadcast({"type": "new_order", "data": new_order.to_dict()})
    return new_order.to_dict()


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@router.get("/", response_model=List[OrderResponse])
async def get_orders():
    return order_service.get_all_orders()


@router.patch("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: str, order_update: OrderUpdate):
    updated_order = order_service.update_order_status(order_id, order_update.status)
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    await manager.broadcast({"type": "order_updated", "data": updated_order.to_dict()})
    return updated_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str):
    if not order_service.delete_order(order_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
