from datetime import datetime
from typing import Optional
from uuid import uuid4
from app.schemas.order import OrderStatus


class Order:
    def __init__(
        self, dish_name: str, quantity: int, special_instructions: Optional[str] = None
    ):
        self.id = str(uuid4())
        self.dish_name = dish_name
        self.quantity = quantity
        self.status = OrderStatus.PENDING
        self.special_instructions = special_instructions
        self.created_at = datetime.utcnow()
        self.updated_at = None

    def update_status(self, status: OrderStatus):
        self.status = status
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "dish_name": self.dish_name,
            "quantity": self.quantity,
            "status": self.status,
            "special_instructions": self.special_instructions,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
