from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Admin

ALGORITHM = "HS256"
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(admin_id: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_ttl_minutes
    )
    payload = {"sub": admin_id, "exp": expires}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def get_current_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Admin:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
    )
    if credentials is None:
        raise unauthorized
    try:
        payload = jwt.decode(
            credentials.credentials, settings.secret_key, algorithms=[ALGORITHM]
        )
    except jwt.PyJWTError as error:
        raise unauthorized from error

    admin = db.get(Admin, payload.get("sub"))
    if admin is None:
        raise unauthorized
    return admin
