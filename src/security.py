import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

SECRET = "my-secret"
ALGORITHM = "HS256"

class AcessToken(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: AcessToken


def sign_jwt(user_id: int) -> dict[str, str]:
    now = time.time()
    payload = {
        "iss": "curso-fastapi.com.br",
        "sub": str(user_id),
        "aud": "curso-fastapi",
        "exp": now + (60 * 30), # 30 minutes
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token}

async def decode_jwt(token: str) -> JWTToken | None:
    try:
        decoded_token = jwt.decode(token, SECRET, audience="curso-fastapi", algorithms=[ALGORITHM])
        _token = JWTToken.model_validate({"access_token": decoded_token})
        return _token if _token.access_token.exp >= time.time() else None
    except Exception as e:
        print(f"decode_jwt error: {e}")
        return None
    

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> HTTPAuthorizationCredentials | None:
        return await super().__call__(request)

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]
) -> dict[str, str]:
    payload = await decode_jwt(credentials.credentials)  # <-- decodifica aqui
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )
    return {"user_id": payload.access_token.sub}


def login_required(current_user: Annotated[dict[str, str], Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return current_user