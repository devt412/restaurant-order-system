from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.services.order import OrderService

router = APIRouter()
order_service = OrderService()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    return order_service.create_order(order)


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
    order = order_service.update_order_status(order_id, order_update.status)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str):
    if not order_service.delete_order(order_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
