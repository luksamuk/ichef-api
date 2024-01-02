from pydantic import BaseModel

class JWTPayload(BaseModel):
    user_id: str
    is_chef: bool
    is_admin: bool
    expires: float

class TokenResponse(BaseModel):
    access_token: str

class Login(BaseModel):
    email: str
    password: str
