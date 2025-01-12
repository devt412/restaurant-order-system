import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from app.main import app

def test_websocket_connection():
    client = TestClient(app)
    try:
        with client.websocket_connect("/api/v1/orders/ws") as websocket:
            # First receive initial data
            initial_data = websocket.receive_json()
            assert initial_data["type"] == "initial_data"
            
            # Then test ping-pong
            websocket.send_text("ping")
            response = websocket.receive_json()
            assert response == {"status": "received"}
    except Exception as e:
        pytest.fail(f"WebSocket connection failed: {str(e)}")

def test_websocket_receives_new_order():
    client = TestClient(app)
    
    with client.websocket_connect("/api/v1/orders/ws") as websocket:
        # First receive initial data
        initial_data = websocket.receive_json()
        assert initial_data["type"] == "initial_data"
        
        # Create new order via HTTP
        order_data = {
            "dish_name": "Test Dish",
            "quantity": 1,
            "special_instructions": "Test instructions"
        }
        response = client.post("/api/v1/orders/", json=order_data)
        assert response.status_code == 201
        
        # Receive WebSocket message for new order
        data = websocket.receive_json()
        
        # Verify the message
        assert data["type"] == "new_order"
        assert data["data"]["dish_name"] == order_data["dish_name"]
        assert data["data"]["quantity"] == order_data["quantity"]

def test_websocket_receives_order_update():
    client = TestClient(app)
    
    # First create an order
    order_data = {
        "dish_name": "Test Dish",
        "quantity": 1,
        "special_instructions": "Test instructions"
    }
    response = client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == 201
    order_id = response.json()["id"]
    
    # Then connect to WebSocket and listen for updates
    with client.websocket_connect("/api/v1/orders/ws") as websocket:
        # First receive initial data
        initial_data = websocket.receive_json()
        assert initial_data["type"] == "initial_data"
        
        # Update the order
        update_data = {"status": "preparing"}
        update_response = client.patch(f"/api/v1/orders/{order_id}", json=update_data)
        assert update_response.status_code == 200
        
        # Receive WebSocket message for update
        data = websocket.receive_json()
        
        # Verify the message
        assert data["type"] == "order_updated"
        assert data["data"]["id"] == order_id
        assert data["data"]["status"] == "preparing"

def test_websocket_connection_multiple_clients():
    client1 = TestClient(app)
    client2 = TestClient(app)
    
    with client1.websocket_connect("/api/v1/orders/ws") as ws1, \
        client2.websocket_connect("/api/v1/orders/ws") as ws2:
        
        # First receive initial data for both clients
        initial_data1 = ws1.receive_json()
        initial_data2 = ws2.receive_json()
        assert initial_data1["type"] == "initial_data"
        assert initial_data2["type"] == "initial_data"
        
        # Create a new order
        order_data = {
            "dish_name": "Test Dish",
            "quantity": 1,
            "special_instructions": "Test instructions"
        }
        response = client1.post("/api/v1/orders/", json=order_data)
        assert response.status_code == 201
        
        # Both clients should receive the new order message
        data1 = ws1.receive_json()
        data2 = ws2.receive_json()
        
        # Verify both clients received the same data
        assert data1 == data2
        assert data1["type"] == "new_order"
        assert data1["data"]["dish_name"] == order_data["dish_name"]

@pytest.fixture(autouse=True)
def clear_orders():
    # Clear orders before each test
    from app.services.order import OrderService
    order_service = OrderService()
    order_service.orders.clear()
    yield
    order_service.orders.clear()