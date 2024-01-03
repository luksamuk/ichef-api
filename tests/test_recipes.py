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

user_payload = None
payloads = None
jwt: str | None = None
chef_jwt: str | None = None

@lru_cache
def load_payloads():
    f = open('tests/recipe_payloads.json')
    return json.load(f)

@pytest.fixture
def prepare_data():
    global payloads
    global user_payload
    global chef_jwt
    
    if payloads is None:
        payloads = load_payloads()
        assert isinstance(payloads, list)

    if chef_jwt is None:
        # Create and save chef
        response = client.post('/users', json=user_data)
        assert response.status_code == 200
        user_payload = response.json()
        
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


@pytest.mark.dependency(depends=["test_create_recipe"])
def test_search_recipe_by_chef(admin_login, prepare_data):
    payload = { "chef_id": user_payload["id"] }
    
    # Do not allow search if not logged in
    response = client.post('/recipes/search', json=payload)
    assert response.status_code == 403
    assert "detail" in response.json()

    # Fail search if not providing any search filters
    response = client.post('/recipes/search', headers=admin_headers(), json={})
    assert response.status_code == 400
    assert "detail" in response.json()

    # Search for chef's recipes using Admin account
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == len(payloads)

    # Search for chef's recipes using Chef's own account
    response = client.post('/recipes/search', headers=chef_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == len(payloads)


@pytest.mark.dependency(depends=["test_create_recipe"])
def test_search_recipe_by_text(admin_login, prepare_data):
    payload = { "text": "torta" }

    # Do not allow search if not logged in
    response = client.post('/recipes/search', json=payload)
    assert response.status_code == 403
    assert "detail" in response.json()

    # Fail search if not providing any search filters
    response = client.post('/recipes/search', headers=admin_headers(), json={})
    assert response.status_code == 400
    assert "detail" in response.json()

    # Search for recipes containing 'torta' using Admin account (two recipes)
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 2

    # Search for recipes containing 'Torta' using Chef's own account (two recipes)
    response = client.post('/recipes/search', headers=chef_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 2

    # Search for recipes containing 'MORANGO' (two recipes)
    payload = { "text": "MORANGO" }
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 2

    # Search for recipes containing 'Sorvete' (one recipe)
    payload = { "text": "Sorvete" }
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 1

    # Search for recipes containing 'calda rala' (one recipe)
    payload = { "text": "calda rala" }
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 1

    # Search for recipes containing 'amendoim' (no recipes)
    payload = { "text": "amendoim" }
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 0

    # Search for recipes containing 'ingredientes' (three recipes)
    payload = { "text": "ingredientes" }
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 3


@pytest.mark.dependency(depends=["test_create_recipe"])
def test_search_recipe_by_chef_and_text(admin_login, prepare_data):
    payload = { "chef_id": user_payload["id"], "text": "torta" }

    # Do not allow search if not logged in
    response = client.post('/recipes/search', json=payload)
    assert response.status_code == 403
    assert "detail" in response.json()

    # Fail search if not providing any search filters
    response = client.post('/recipes/search', headers=admin_headers(), json={})
    assert response.status_code == 400
    assert "detail" in response.json()

    # Search for recipes containing 'torta' using Admin account (two recipes)
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 2

    # Search for recipes containing 'Torta' using Chef's own account (two recipes)
    response = client.post('/recipes/search', headers=chef_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 2

    # Search for recipes containing 'MORANGO' (two recipes)
    payload["text"] = "MORANGO"
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 2

    # Search for recipes containing 'Sorvete' (one recipe)
    payload["text"] = "Sorvete"
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 1

    # Search for recipes containing 'calda rala' (one recipe)
    payload["text"] = "calda rala"
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 1

    # Search for recipes containing 'amendoim' (no recipes)
    payload["text"] = "amendoim"
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 0

    # Search for recipes containing 'ingredientes' (three recipes)
    payload["text"] = "ingredientes"
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 3
    pass


@pytest.mark.skip(reason="Unimplemented")
@pytest.mark.dependency(depends=[
    "test_search_recipe_by_text",
    "test_search_recipe_by_chef",
    "test_search_recipe_by_chef_and_text",
])
def test_update_recipe(admin_login, prepare_data):
    # Search for a single recipe containing 'calda rala'
    payload = { "text": "calda rala" }
    response = client.post('/recipes/search', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 1
    recipe = res[0]

    route = '/recipe/' + recipe["id"]

    # Do not allow changing anything if you're not logged in
    response = client.put(route, json={"title": "This Should Fail"})
    assert response.status_code == 403
    assert "detail" in response.json()

    # Change name as Admin
    response = client.put(route, headers=admin_headers(), json={
        "title": "New Admin Recipe Name",
    })
    assert response.status_code == 200
    check_response_valid(response.json())
    assert response.json()["title"] == "New Admin Recipe Name"

    # Change text as Admin
    response = client.put(route, headers=admin_headers(), json={
        "text": "This is my new admin recipe.",
    })
    assert response.status_code == 200
    check_response_valid(response.json())
    assert response.json()["text"] == "This is my new admin recipe."

    # Change name and text as Admin
    response = client.put(route, headers=admin_headers(), json={
        "name": "My Admin Recipe",
        "text": "This is an admin recipe."
    })
    assert response.status_code == 200
    check_response_valid(response.json())
    assert response.json()["title"] == "My Admin Recipe"
    assert response.json()["text"] == "This is an admin recipe."

    # Change name as chef (recipe owner)
    response = client.put(route, headers=chef_headers(), json={
        "title": "New Chef Recipe Name",
    })
    assert response.status_code == 200
    check_response_valid(response.json())
    assert response.json()["title"] == "New Chef Recipe Name"

    # Change text as chef (recipe owner)
    response = client.put(route, headers=chef_headers(), json={
        "text": "This is my new chef recipe.",
    })
    assert response.status_code == 200
    check_response_valid(response.json())
    assert response.json()["text"] == "This is my new chef recipe."

    # Change name and text as chef
    response = client.put(route, headers=chef_headers(), json={
        "name": "My Chef Recipe",
        "text": "This is a chef recipe."
    })
    assert response.status_code == 200
    check_response_valid(response.json())
    assert response.json()["title"] == "My Chef Recipe"
    assert response.json()["text"] == "This is a chef recipe."


@pytest.mark.dependency(depends=["test_update_recipe"])
def test_delete_recipe(admin_login, prepare_data):
    # Find all recipes by the chef
    response = client.post('/recipes/search', headers=admin_headers(), json={
        "chef_id": user_payload["id"]
    })
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 3
    recipe = res[0]

    route = '/recipes/' + recipe["id"]
    
    # Do not allow deleting recipe if not logged in
    response = client.delete(route)
    assert response.status_code == 403
    assert "detail" in response.json()

    # Delete first recipe
    response = client.delete(route, headers=admin_headers())
    assert response.status_code == 204

    # Check if number of recipes decreased
    response = client.post('/recipes/search', headers=admin_headers(), json={
        "chef_id": user_payload["id"]
    })
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 2

    # Delete chef
    response = client.delete('/users/' + user_payload["id"], headers=admin_headers())
    assert response.status_code == 204

    # Check if all recipes were deleted as well
    response = client.post('/recipes/search', headers=admin_headers(), json={
        "chef_id": user_payload["id"]
    })
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(res) == 0


