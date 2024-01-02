from pydantic import BaseModel

class JWTPayload:
    user_id: str
    expires: float

class TokenResponse:
    access_token: str

class Login(BaseModel):
    email: str
    password: str
