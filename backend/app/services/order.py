from typing import List, Optional
from ..models.order import Order
from ..schemas.order import OrderStatus, OrderCreate, OrderUpdate


class OrderService:
    def __init__(self):
        self.orders: dict[str, Order] = {}

    def create_order(self, order_data: OrderCreate) -> Order:
        order = Order(
            dish_name=order_data.dish_name,
            quantity=order_data.quantity,
            special_instructions=order_data.special_instructions,
        )
        self.orders[order.id] = order
        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)

    def get_all_orders(self) -> List[Order]:
        return list(self.orders.values())

    def update_order_status(
        self, order_id: str, status: OrderStatus
    ) -> Optional[Order]:
        order = self.orders.get(order_id)
        if order:
            order.update_status(status)
        return order

    def delete_order(self, order_id: str) -> bool:
        if order_id in self.orders:
            del self.orders[order_id]
            return True
        return False
