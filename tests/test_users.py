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

jwt: str | None = None

payloads = {
    "admin": {
	"name": "Admin Test",
	"email": "admin@test.com",
	"password": "PKPF1wyLhpG3CSL_ND4xg8EJowi-vhzK",
	"is_chef": False,
	"is_admin": True,
    },
    "chef": {
	"name": "Chef Test",
	"email": "chef@test.com",
	"password": "uyMP28LJB5rKK6gZ85qJAoLoZUj17bSU",
	"is_chef": True,
	"is_admin": False,
    }
}

def check_response_valid(response):
    assert "name" in response
    assert "email" in response
    assert "is_chef" in response
    assert "is_admin" in response
    assert "id" in response
    assert "created_at" in response
    assert "updated_at" in response
    assert "password" not in response
    assert "pw_hash" not in response

def check_response_corresponds_payload(response, payload):
    check_response_valid(response)
    assert response["name"] == payload["name"]
    assert response["email"] == payload["email"]
    assert response["is_chef"] == payload["is_chef"]
    assert response["is_admin"] == payload["is_admin"]
    assert is_valid_uuid(response["id"])

def admin_headers():
    return { "Authorization": "Bearer " + jwt }

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


@pytest.mark.dependency()
def test_create_admin(admin_login):
    payload = payloads["admin"]
    
    # Do not allow creating an admin if not logged in as an admin
    response = client.post('/users/admin', json=payload)
    assert response.status_code == 403
    assert "detail" in response.json()

    # Create admin
    response = client.post('/users/admin', headers=admin_headers(), json=payload)
    assert response.status_code == 200
    check_response_corresponds_payload(response.json(), payload)

    # Do not allow creating the same user again
    response = client.post('/users/admin', headers=admin_headers(), json=payload)
    assert response.status_code == 409
    assert "detail" in response.json()


@pytest.mark.dependency()
def test_create_chef(admin_login):
    payload = payloads["chef"]
    response = client.post('/users', json=payload)
    assert response.status_code == 200
    check_response_corresponds_payload(response.json(), payload)

    # Do not allow creating the same user again
    response = client.post('/users', json=payload)
    assert response.status_code == 409
    assert "detail" in response.json()


@pytest.mark.dependency(depends=["test_create_admin", "test_create_chef"])
def test_list_users(admin_login):
    # Do not allow listing users without credentials
    response = client.get('/users')
    assert response.status_code == 403
    assert "detail" in response.json()

    # Perform listing
    response = client.get('/users', headers=admin_headers())
    assert response.status_code == 200
    res = response.json()
    
    assert isinstance(res, list)
    #assert len(res) == 2

    found_admin = False
    found_chef = False
    for elt in res:
        payload = {}
        if elt["email"] == "admin@test.com":
            assert not found_admin
            found_admin = True
            payload = payloads["admin"]
        elif elt["email"] == "chef@test.com":
            assert not found_chef
            found_chef = True
            payload = payloads["chef"]
        else:
            # Ignore other entities from other tests
            continue
            #raise Exception('Unknown entity. Is the database clean?')

        check_response_corresponds_payload(elt, payload)


@pytest.mark.dependency(depends=["test_create_admin", "test_create_chef"])
def test_recover_user(admin_login):
    for _, payload in payloads.items():
        # Do not allow recovering users by e-mail without authentication
        response = client.get('/users/email/' + payload["email"])
        assert response.status_code == 403
        assert "detail" in response.json()
        
        # Recover user by e-mail
        response = client.get(
            '/users/email/' + payload["email"],
            headers=admin_headers(),
        )
        assert response.status_code == 200
        check_response_corresponds_payload(response.json(), payload)

        # Recover same user, this time by ID
        id = response.json()["id"]

        # Do not allow recovering users by id without authentication
        response2 = client.get('/users/' + id)
        assert response2.status_code == 403
        assert "detail" in response2.json()
        
        # Recover user with credentials
        response2 = client.get('/users/' + id, headers=admin_headers())
        assert response2.status_code == 200
        check_response_corresponds_payload(response2.json(), payload)


@pytest.mark.dependency(depends=["test_list_users", "test_recover_user"])
def test_update_user(admin_login):
    # We'll modify the users, so any recovery/listing tests
    # need to be finished at this point
    for _, payload in payloads.items():
        # Fetch old user by e-mail
        response = client.get(
            '/users/email/' + payload["email"],
            headers=admin_headers(),
        )
        assert response.status_code == 200
        orig_user = response.json()
        check_response_corresponds_payload(orig_user, payload)

        route = '/users/' + orig_user["id"]

        alt_user = {
            "name": orig_user["name"] + ' (changed)',
            "email": orig_user["email"],
            "password": "DE_gf-IM2VoLvBPZozufqOHNWRMo33rg",
            "is_chef": orig_user["is_chef"],
            "is_admin": not orig_user["is_admin"],
        }

        # Do not allow updating anything without credentials
        response = client.put(
            route,
            json={ "name": alt_user["name"] },
        )
        assert response.status_code == 403
        assert "detail" in response.json()

        # Update name
        response = client.put(
            route,
            headers=admin_headers(),
            json={ "name": alt_user["name"] },
        )
        assert response.status_code == 200
        new_user = response.json()
        check_response_valid(new_user)
        assert new_user["name"] == alt_user["name"]

        # Update admin status
        response = client.put(
            route,
            headers=admin_headers(),
            json={ "is_admin": alt_user["is_admin"] },
        )
        assert response.status_code == 200
        new_user = response.json()
        check_response_valid(new_user)
        assert new_user["is_admin"] == alt_user["is_admin"]

        # Update password
        response = client.put(
            route,
            headers=admin_headers(),
            json={
                "old_password": payload["password"],
                "password": alt_user["password"],
            },
        )
        assert response.status_code == 200
        new_user = response.json()
        check_response_valid(new_user)

        # Do not allow changing password if old password was not provided.
        response = client.put(
            route,
            headers=admin_headers(),
            json={ "password": "moK2tza_yTdKj5HM4U8sZUjx3KRrAYS2" },
        )
        assert response.status_code == 401
        assert "detail" in response.json()
        
        # Do not allow changing password if old password is incorrect.
        response = client.put(
            route,
            headers=admin_headers(),
            json={
                "old_password": "incorrectpassword",
                "password": "aKJaIJET4RHSOjaG70xtZ4IzTwcJP3gb",
            },
        )
        assert response.status_code == 401
        assert "detail" in response.json()
        
        # Do not allow changing chef status.
        response = client.put(
            route,
            headers=admin_headers(),
            json={ "is_chef": not orig_user["is_chef"] },
        )
        assert response.status_code == 400
        assert "detail" in response.json()
        
        # Do not allow changing e-mail.
        response = client.put(
            route,
            headers=admin_headers(),
            json={ "email": "weirdmail@weird.com" },
        )
        assert response.status_code == 400
        assert "detail" in response.json()

@pytest.mark.skip(reason="Unimplemented")
@pytest.mark.dependency(depends=["test_update_user"])
def test_disable_user(admin_login):
    pass

@pytest.mark.skip(reason="Unimplemented")
@pytest.mark.dependency(depends=["test_disable_user"])
def test_remove_user(admin_login):
    pass

