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
    
@pytest.mark.dependency()
def test_create_admin():
    payload = payloads["admin"]
    
    response = client.post(
        '/users',
        json=payload,
    )

    assert response.status_code == 200

    res = response.json()
    assert res["name"] == payload["name"]
    assert res["email"] == payload["email"]
    assert res["is_chef"] == payload["is_chef"]
    assert res["is_admin"] == payload["is_admin"]
    assert "password" not in res
    assert "pw_hash" not in res
    assert "id" in res
    assert is_valid_uuid(res["id"])

@pytest.mark.dependency()
def test_create_chef():
    payload = payloads["chef"]

    response = client.post(
        '/users',
        json=payload,
    )

    assert response.status_code == 200

    res = response.json()
    assert res["name"] == payload["name"]
    assert res["email"] == payload["email"]
    assert res["is_chef"] == payload["is_chef"]
    assert res["is_admin"] == payload["is_admin"]
    assert "password" not in res
    assert "pw_hash" not in res
    assert "id" in res
    assert is_valid_uuid(res["id"])


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
        
        assert elt["name"] == payload["name"]
        assert elt["email"] == payload["email"]
        assert elt["is_chef"] == payload["is_chef"]
        assert elt["is_admin"] == payload["is_admin"]
        assert "password" not in elt
        assert "pw_hash" not in elt
        assert "id" in elt
        assert is_valid_uuid(elt["id"])
        
