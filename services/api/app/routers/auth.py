import re
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import RequestContext, get_request_context
from app.models import Membership, User, Workspace
from app.schemas import (
    CurrentUserResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.security import create_access_token, hash_password, verify_password


router = APIRouter(prefix="/v1/auth", tags=["auth"])


def make_slug(name: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "workspace"
    return f"{base}-{uuid4().hex[:8]}"


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    email = payload.email.lower().strip()
    if db.scalar(select(User).where(User.email == email)) is not None:
        raise HTTPException(status_code=409, detail="An account with this email already exists")

    user = User(
        email=email,
        full_name=payload.full_name.strip(),
        password_hash=hash_password(payload.password),
    )
    workspace = Workspace(name=payload.workspace_name.strip(), slug=make_slug(payload.workspace_name))
    db.add_all([user, workspace])
    db.flush()

    membership = Membership(user_id=user.id, workspace_id=workspace.id, role="owner")
    db.add(membership)
    db.commit()

    return TokenResponse(
        access_token=create_access_token(user.id, workspace.id, membership.role)
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email.lower().strip()))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    membership = db.scalar(
        select(Membership).where(Membership.user_id == user.id).order_by(Membership.id)
    )
    if membership is None:
        raise HTTPException(status_code=403, detail="Account has no workspace access")

    return TokenResponse(
        access_token=create_access_token(user.id, membership.workspace_id, membership.role)
    )


@router.get("/me", response_model=CurrentUserResponse)
def me(context: RequestContext = Depends(get_request_context)) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=context.user.id,
        email=context.user.email,
        full_name=context.user.full_name,
        workspace_id=context.workspace.id,
        workspace_name=context.workspace.name,
        role=context.membership.role,
    )
