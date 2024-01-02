import time
import jwt
from uuid import UUID
from config.settings import get_settings
from schemas.auth import JWTPayload, TokenResponse

settings = get_settings()

def jwt_sign(user_id: UUID) -> TokenResponse:
    payload = JWTPayload(
        user_id=str(user_id),
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

