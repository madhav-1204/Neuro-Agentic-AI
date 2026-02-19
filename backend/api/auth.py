import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from app.config.settings import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    GOOGLE_CLIENT_ID,
)
from app.database import upsert_user, get_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer(auto_error=False)


class GoogleTokenRequest(BaseModel):
    token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class UserInfo(BaseModel):
    email: str
    name: str
    picture: str


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token — raises 401 if missing or invalid."""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        # Verify user still exists in DB
        user = get_user(email)
        if not user:
            raise HTTPException(status_code=401, detail="User no longer exists")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


def verify_token_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Verify JWT if present; returns payload or None for anonymous access."""
    if credentials is None:
        return None
    try:
        payload = jwt.decode(token=credentials.credentials, key=SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


@router.post("/google", response_model=TokenResponse)
async def google_auth(token_request: GoogleTokenRequest):
    """Authenticate user with Google OAuth token"""
    try:
        # Verify the Google token
        idinfo = id_token.verify_oauth2_token(
            token_request.token, requests.Request(), GOOGLE_CLIENT_ID
        )

        # Extract user information
        email = idinfo.get("email")
        name = idinfo.get("name")
        picture = idinfo.get("picture")

        if not email:
            raise HTTPException(status_code=400, detail="Email not found in token")

        # Store/update user in SQLite database
        user_data = upsert_user(email, name, picture)

        # Create JWT token
        access_token = create_access_token(
            data={"sub": email, "name": name, "picture": picture}
        )

        logger.info("User authenticated: %s", email)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_data,
        )

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")


@router.get("/me", response_model=UserInfo)
async def get_current_user(token_data: dict = Depends(verify_token)):
    """Get current user information"""
    return UserInfo(
        email=token_data.get("sub"),
        name=token_data.get("name"),
        picture=token_data.get("picture"),
    )


@router.post("/logout")
async def logout(token_data: dict = Depends(verify_token)):
    """Logout user (client should delete token)"""
    logger.info("User logged out: %s", token_data.get("sub"))
    return {"message": "Successfully logged out"}
