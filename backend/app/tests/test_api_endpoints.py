import pytest
from fastapi.testclient import TestClient
from app.schemas.order import OrderStatus


def test_create_order_api(test_client, sample_order_data):
    # When
    response = test_client.post("/api/v1/orders/", json=sample_order_data)

    # Then
    assert response.status_code == 201
    data = response.json()
    assert data["dish_name"] == sample_order_data["dish_name"]
    assert data["quantity"] == sample_order_data["quantity"]
    assert data["status"] == OrderStatus.PENDING


def test_create_order_invalid_data(test_client):
    # Given
    invalid_data = {
        "dish_name": "",  # Empty name should be invalid
        "quantity": 0,  # Zero quantity should be invalid
    }

    # When
    response = test_client.post("/api/v1/orders/", json=invalid_data)

    # Then
    assert response.status_code == 422  # Validation error


def test_get_orders_api(test_client, sample_order_data):
    # Given
    test_client.post("/api/v1/orders/", json=sample_order_data)

    # When
    response = test_client.get("/api/v1/orders/")

    # Then
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert isinstance(data, list)


def test_update_order_status_api(test_client, sample_order_data):
    # Given
    create_response = test_client.post("/api/v1/orders/", json=sample_order_data)
    order_id = create_response.json()["id"]

    # When
    update_data = {"status": OrderStatus.PREPARING}
    response = test_client.patch(f"/api/v1/orders/{order_id}", json=update_data)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == OrderStatus.PREPARING


def test_update_nonexistent_order_api(test_client):
    # When
    update_data = {"status": OrderStatus.PREPARING}
    response = test_client.patch("/api/v1/orders/nonexistent-id", json=update_data)

    # Then
    assert response.status_code == 404
