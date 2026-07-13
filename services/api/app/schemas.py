from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=160)
    password: str = Field(min_length=10, max_length=128)
    workspace_name: str = Field(min_length=2, max_length=160)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    workspace_id: str
    workspace_name: str
    role: str


class WatchlistItemCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=40)
    exchange: str = Field(default="NSE", min_length=2, max_length=20)
    note: str | None = Field(default=None, max_length=500)


class WatchlistItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    symbol: str
    exchange: str
    note: str | None
    created_at: datetime


class HoldingCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=40)
    exchange: str = Field(default="NSE", min_length=2, max_length=20)
    quantity: float = Field(gt=0)
    average_price: float = Field(ge=0)


class HoldingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    symbol: str
    exchange: str
    quantity: float
    average_price: float


class PortfolioCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    base_currency: str = Field(default="INR", min_length=3, max_length=3)


class PortfolioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    base_currency: str
    created_at: datetime
    holdings: list[HoldingResponse] = []
