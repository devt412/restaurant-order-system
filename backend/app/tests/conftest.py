import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.order import OrderService
from app.schemas.order import OrderCreate


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def order_service():
    return OrderService()


@pytest.fixture
def sample_order_data():
    return {
        "dish_name": "Test Dish",
        "quantity": 2,
        "special_instructions": "Test instructions",
    }


@pytest.fixture
def created_order(order_service, sample_order_data):
    order_create = OrderCreate(**sample_order_data)
    return order_service.create_order(order_create)
