import pytest
from app.schemas.order import OrderCreate, OrderStatus
from app.services.order import OrderService


def test_create_order(order_service, sample_order_data):
    # Given
    order_create = OrderCreate(**sample_order_data)

    # When
    order = order_service.create_order(order_create)

    # Then
    assert order.dish_name == sample_order_data["dish_name"]
    assert order.quantity == sample_order_data["quantity"]
    assert order.special_instructions == sample_order_data["special_instructions"]
    assert order.status == OrderStatus.PENDING


def test_get_order(order_service, created_order):
    # When
    retrieved_order = order_service.get_order(created_order.id)

    # Then
    assert retrieved_order is not None
    assert retrieved_order.id == created_order.id
    assert retrieved_order.dish_name == created_order.dish_name


def test_get_nonexistent_order(order_service):
    # When
    retrieved_order = order_service.get_order("nonexistent-id")

    # Then
    assert retrieved_order is None


def test_get_all_orders(order_service, sample_order_data):
    # Given
    order_create = OrderCreate(**sample_order_data)
    order_service.create_order(order_create)
    order_service.create_order(order_create)

    # When
    orders = order_service.get_all_orders()

    # Then
    assert len(orders) == 2
    assert all(order.dish_name == sample_order_data["dish_name"] for order in orders)


def test_update_order_status(order_service, created_order):
    # When
    updated_order = order_service.update_order_status(
        created_order.id, OrderStatus.PREPARING
    )

    # Then
    assert updated_order is not None
    assert updated_order.status == OrderStatus.PREPARING
    assert updated_order.updated_at is not None


def test_update_nonexistent_order_status(order_service):
    # When
    updated_order = order_service.update_order_status(
        "nonexistent-id", OrderStatus.PREPARING
    )

    # Then
    assert updated_order is None


def test_delete_order(order_service, created_order):
    # When
    result = order_service.delete_order(created_order.id)

    # Then
    assert result is True
    assert order_service.get_order(created_order.id) is None


def test_delete_nonexistent_order(order_service):
    # When
    result = order_service.delete_order("nonexistent-id")

    # Then
    assert result is False
