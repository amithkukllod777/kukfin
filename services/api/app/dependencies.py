from dataclasses import dataclass

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Membership, User, Workspace
from app.security import decode_access_token


bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class RequestContext:
    user: User
    workspace: Workspace
    membership: Membership


def get_request_context(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> RequestContext:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = str(payload["sub"])
        workspace_id = str(payload["workspace_id"])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError):
        raise unauthorized from None

    membership = db.scalar(
        select(Membership).where(
            Membership.user_id == user_id,
            Membership.workspace_id == workspace_id,
        )
    )
    if membership is None:
        raise unauthorized

    user = db.get(User, user_id)
    workspace = db.get(Workspace, workspace_id)
    if user is None or workspace is None:
        raise unauthorized

    return RequestContext(user=user, workspace=workspace, membership=membership)
