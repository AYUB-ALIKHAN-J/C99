import sys
import os
import pytest

# Ensure the project root is in sys.path so 'main' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_service(client):
    response = client.post('/services', json={
        "name": {"en": "Test Hall"},
        "description": {"en": "A test hall"},
        "category": "venue",
        "vendor_id": "vendor1"
    })
    assert response.status_code == 201
    assert "data" in response.get_json()
    global service_id
    service_id = response.get_json()["data"]["id"]

def test_list_services(client):
    response = client.get('/services')
    assert response.status_code == 200
    assert "data" in response.get_json()
    assert isinstance(response.get_json()["data"], list)

def test_get_service_details(client):
    # Use the first service from the list
    response = client.get('/services')
    assert response.status_code == 200
    services = response.get_json()["data"]
    if services:
        sid = services[0]["id"]
        detail_resp = client.get(f'/services/{sid}')
        assert detail_resp.status_code == 200
        assert "data" in detail_resp.get_json()
    else:
        pytest.skip("No services to test details.")

def test_update_service(client):
    response = client.get('/services')
    services = response.get_json()["data"]
    if services:
        sid = services[0]["id"]
        update_resp = client.put(f'/services/{sid}', json={"name": {"en": "Updated Hall"}})
        assert update_resp.status_code == 200
        assert "data" in update_resp.get_json()
        assert update_resp.get_json()["data"]["name"]["en"] == "Updated Hall"
    else:
        pytest.skip("No services to update.")

def test_delete_service(client):
    response = client.get('/services')
    services = response.get_json()["data"]
    if services:
        sid = services[0]["id"]
        del_resp = client.delete(f'/services/{sid}')
        assert del_resp.status_code == 200
        assert "message" in del_resp.get_json()
    else:
        pytest.skip("No services to delete.")

def test_create_vendor(client):
    response = client.post('/vendors', json={
        "name": "Test Vendor",
        "contact": {"email": "test@vendor.com"},
        "rating": {"average": 5.0, "count": 1}
    })
    assert response.status_code == 201
    assert "data" in response.get_json()
    global vendor_id
    vendor_id = response.get_json()["data"]["id"]

def test_list_vendors(client):
    response = client.get('/vendors')
    assert response.status_code == 200
    assert "data" in response.get_json()
    assert isinstance(response.get_json()["data"], list)

def test_get_vendor_details(client):
    response = client.get('/vendors')
    vendors = response.get_json()["data"]
    if vendors:
        vid = vendors[0]["id"]
        detail_resp = client.get(f'/vendors/{vid}')
        assert detail_resp.status_code == 200
        assert "data" in detail_resp.get_json()
    else:
        pytest.skip("No vendors to test details.")

def test_update_vendor(client):
    response = client.get('/vendors')
    vendors = response.get_json()["data"]
    if vendors:
        vid = vendors[0]["id"]
        update_resp = client.put(f'/vendors/{vid}', json={"name": "Updated Vendor"})
        assert update_resp.status_code == 200
        assert "data" in update_resp.get_json()
        assert update_resp.get_json()["data"]["name"] == "Updated Vendor"
    else:
        pytest.skip("No vendors to update.")

def test_delete_vendor(client):
    response = client.get('/vendors')
    vendors = response.get_json()["data"]
    if vendors:
        vid = vendors[0]["id"]
        del_resp = client.delete(f'/vendors/{vid}')
        assert del_resp.status_code == 200
        assert "message" in del_resp.get_json()
    else:
        pytest.skip("No vendors to delete.")

def test_search_services(client):
    response = client.get('/services/search?q=Test')
    assert response.status_code == 200
    assert "data" in response.get_json()
    assert isinstance(response.get_json()["data"], list)
