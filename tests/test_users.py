import pytest
from main import app
from fastapi.testclient import TestClient
from uuid import UUID

# To generate random passwords on Linux console:
#  $ < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32};echo;

client = TestClient(app)


def is_valid_uuid(val: str) -> bool:
    try:
        UUID(val)
        return True
    except ValueError:
        return False


payloads = {
    "admin": {
	"name": "Admin Test",
	"email": "admin@admin.com",
	"password": "PKPF1wyLhpG3CSL_ND4xg8EJowi-vhzK",
	"is_chef": False,
	"is_admin": True,
    },
    "chef": {
	"name": "Chef Test",
	"email": "chef@chef.com",
	"password": "uyMP28LJB5rKK6gZ85qJAoLoZUj17bSU",
	"is_chef": True,
	"is_admin": False,
    }
}

def check_response_valid(response, payload):
    assert "name" in response
    assert "email" in response
    assert "is_chef" in response
    assert "is_admin" in response
    assert "id" in response
    assert "password" not in response
    assert "pw_hash" not in response
    
    assert response["name"] == payload["name"]
    assert response["email"] == payload["email"]
    assert response["is_chef"] == payload["is_chef"]
    assert response["is_admin"] == payload["is_admin"]
    assert is_valid_uuid(response["id"])


@pytest.mark.dependency()
def test_create_admin():
    payload = payloads["admin"]
    
    response = client.post(
        '/users',
        json=payload,
    )

    assert response.status_code == 200
    check_response_valid(response.json(), payload)


@pytest.mark.dependency()
def test_create_chef():
    payload = payloads["chef"]

    response = client.post(
        '/users',
        json=payload,
    )

    assert response.status_code == 200
    check_response_valid(response.json(), payload)


@pytest.mark.dependency(depends=["test_create_admin", "test_create_chef"])
def test_list_users():
    response = client.get('/users')
    assert response.status_code == 200
    res = response.json()
    
    assert isinstance(res, list)
    assert len(res) == 2

    found_admin = False
    found_chef = False
    for elt in res:
        payload = {}
        if elt["email"] == "admin@admin.com":
            assert not found_admin
            found_admin = True
            payload = payloads["admin"]
        elif elt["email"] == "chef@chef.com":
            assert not found_chef
            found_chef = True
            payload = payloads["chef"]
        else:
            raise Exception('Unknown entity. Is the database clean?')

        check_response_valid(elt, payload)


@pytest.mark.dependency(depends=["test_create_admin", "test_create_chef"])
def test_recover_user():
    for payload in payloads:
        # Recover user by e-mail
        response = client.get('/users/email/' + payload["email"])
        assert response.status_code == 200
        check_response_valid(response.json(), payload)

        # Recover same user, this time by ID
        id = response.json()["id"]
        response2 = client.get('/users/' + id)
        assert response2.status_code == 200
        check_response_valid(response2.json(), payload)

