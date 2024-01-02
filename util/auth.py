import time
import jwt
from uuid import UUID
from config.settings import get_settings
from schemas.auth import JWTPayload, TokenResponse
from model.users import User

settings = get_settings()

def jwt_sign(data: User) -> TokenResponse:
    payload = JWTPayload(
        user_id=str(data.id),
        is_chef = data.is_chef,
        is_admin = data.is_admin,
        expires=time.time() + settings.jwt_expiry_seconds,
    )
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return TokenResponse(access_token=token)

def jwt_decode(token: str) -> JWTPayload:
    decoded = jwt.decode(token, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return JWTPayload(
        user_id=decoded["user_id"],
        expires=float(decoded["expires"]),
    )

def jwt_validate(payload: JWTPayload) -> bool:
    return payload.expires >= time.time()

