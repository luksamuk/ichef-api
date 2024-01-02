from main import app
from fastapi.testclient import TestClient
import tests.test_util

client = TestClient(app)

def test_create_user():
    payload = {
	"name": "Fulano de Tal",
	"email": "fulano@exemplo.com",
	"password": "senha1234",
	"is_chef": True,
	"is_admin": True,
    }

    response = client.post(
        '/users',
        #TODO: headers={...}
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
    
