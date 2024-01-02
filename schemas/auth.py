from pydantic import BaseModel

class JWTPayload:
    user_id: str
    is_chef: bool
    is_admin: bool
    expires: float

class TokenResponse:
    access_token: str

class Login(BaseModel):
    email: str
    password: str
