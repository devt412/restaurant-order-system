from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderCreate(BaseModel):
    dish_name: str = Field(..., min_length=2, description="Name of the dish")
    quantity: int = Field(..., gt=0, description="Quantity of dishes ordered")
    special_instructions: Optional[str] = Field(None, max_length=500)


class OrderUpdate(BaseModel):
    status: OrderStatus
    special_instructions: Optional[str] = Field(None, max_length=500)


class OrderResponse(BaseModel):
    id: str
    dish_name: str
    quantity: int
    status: OrderStatus
    special_instructions: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
