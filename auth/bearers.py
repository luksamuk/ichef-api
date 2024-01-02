from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from util.auth import jwt_decode, jwt_validate
from schemas.auth import JWTPayload

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials =\
            await super(JWTBearer, self).__call__(request)

        if not credentials:
            raise HTTPException(status_code=403, detail='Invalid credentials')

        if not credentials.scheme == 'Bearer':
            raise HTTPException(status_code=403, detail='Invalid authentication scheme')

        if not self.verify(credentials.credentials):
            raise HTTPException(status_code=403, detail='Invalid authorization token')

        return credentials.credentials

    
    def verify(self, jwt: str) -> bool:
        try:
            payload = jwt_decode(jwt)
            return jwt_validate(payload)
        except:
            # TODO: Log exception to console. We never know what's going
            # to happen
            return False


