import pytest
import json
from main import app
from fastapi.testclient import TestClient
from uuid import UUID, uuid4
from functools import lru_cache

client = TestClient(app)

def is_valid_uuid(val: str) -> bool:
    try:
        UUID(val)
        return True
    except ValueError:
        return False

# Default payloads
user_data = {
    "name": "Chef Recipes",
    "email": "chef_recipes@recipes.com",
    "password": "IWaLuzLTWbK6qRvl8grfnNZwguXnGW0R",
    "is_chef": True,
    "is_admin": False,
}

payloads = None
user = None

@lru_cache
def load_payloads():
    f = open('tests/recipe_payloads.json')
    return json.load(f)

@pytest.fixture
def prepare_data():
    global payloads
    global user
    
    if payloads is None:
        payloads = load_payloads()
    if user is None:
        response = client.post('/users', json=user_data)
        assert response.status_code == 200
        user = response.json()
        assert "id" in user

    # Set chef_id in all recipes
    for payload in payloads:
        payload["chef_id"] = user["id"]



def check_response_valid(response):
    assert "chef_id" in response
    assert "title" in response
    assert "text" in response
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response

def check_response_corresponds_payload(response, payload):
    check_response_valid(response)
    assert response["chef_id"] == payload["chef_id"]
    assert response["title"] == payload["title"]
    assert response["text"] == payload["text"]
    assert is_valid_uuid(response["id"])
        
@pytest.mark.dependency()
def test_create_recipe(prepare_data):
    # Create a non-chef user
    response = client.post(
        '/users',
        json={
            "name": "Common User",
            "email": "commonuser@example.com",
            "password": "H651A8oKgNrER-SURvYvrDTLBChUdGCl",
            "is_chef": False,
            "is_admin": False,
        }
    )
    assert response.status_code == 200
    commonuser = response.json()
    assert "id" in commonuser

    # Test every recipe payload
    for recipe in payloads:
        payload = recipe.copy()
        response = client.post('/recipes', json=payload)
        assert response.status_code == 200
        check_response_corresponds_payload(response.json(), payload)

        # Do not allow creating a recipe for a chef that does not exist
        payload["chef_id"] = str(uuid4())
        response = client.post('/recipes', json=payload)
        assert response.status_code == 404
        assert "detail" in response.json()

        # Do not allow creating a recipe for a user that is not a chef
        payload["chef_id"] = commonuser["id"]
        response = client.post('/recipes', json=payload)
        assert response.status_code == 400
        assert "detail" in response.json()

    # TODO: Delete this extra user
    # TODO

