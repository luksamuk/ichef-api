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
}

payloads = None
user = None
jwt: str | None = None
chef_jwt: str | None = None

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

    if chef_jwt is None:
        response = client.post('/users', json=user_data)
        assert response.status_code == 200
        # Perform login
        response = client.post(
            '/auth/token',
            json={ "email": user_data["email"], "password": user_data["password"] },
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        chef_jwt = response.json()["access_token"]

@pytest.fixture
def admin_login():
    global jwt
    if jwt is None:
        payload = { "email": "admin@admin.com", "password": "admin" }
        response = client.post('/auth/token', json=payload)
        assert response.status_code == 200
        json = response.json()
        assert "access_token" in json
        jwt = json["access_token"]

def admin_headers():
    return { "Authorization": "Bearer " + jwt }

def chef_headers():
    return { "Authorization": "Bearer " + chef_jwt }
        
def check_response_valid(response):
    assert "chef_id" in response
    assert "title" in response
    assert "text" in response
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response

def check_response_corresponds_payload(response, payload):
    check_response_valid(response)
    assert response["title"] == payload["title"]
    assert response["text"] == payload["text"]
    assert is_valid_uuid(response["id"])
        
@pytest.mark.dependency()
def test_create_recipe(admin_login, prepare_data):
    # Test every recipe payload
    for recipe in payloads:
        response = client.post('/recipes', headers=chef_headers(), json=recipe)
        assert response.status_code == 200
        check_response_corresponds_payload(response.json(), recipe)

        # Do not allow creating a recipe for a user that is not a chef
        response = client.post('/recipes', headers=admin_headers(), json=recipe)
        assert response.status_code == 400
        assert "detail" in response.json()


@pytest.mark.skip(reason="Unimplemented")
@pytest.mark.dependency()
def test_update_recipe(admin_login, prepare_data):
    pass

@pytest.mark.skip(reason="Unimplemented")
@pytest.mark.dependency()
def test_search_recipe_by_chef(admin_login, prepare_data):
    pass

@pytest.mark.skip(reason="Unimplemented")
@pytest.mark.dependency()
def test_search_recipe_by_text(admin_login, prepare_data):
    pass

@pytest.mark.skip(reason="Unimplemented")
@pytest.mark.dependency()
def test_search_recipe_by_chef_and_text(admin_login, prepare_data):
    pass

@pytest.mark.skip(reason="Unimplemented")
@pytest.mark.dependency()
def test_delete_recipe(admin_login, prepare_data):
    pass

