from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text

from app.core.config import get_settings
from app.db import Base, engine
from app.routers import auth, portfolios, watchlists


settings = get_settings()


class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: datetime


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Alembic migrations will replace create_all before the first production deployment.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="SaaS gateway for KukFin research and portfolio intelligence.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(watchlists.router)
app.include_router(portfolios.router)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="kukfin-api",
        timestamp=datetime.now(UTC),
    )


@app.get("/ready", tags=["system"])
def readiness() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ready", "database": "connected"}


@app.get("/v1/system/capabilities", tags=["system"])
def capabilities() -> dict[str, object]:
    return {
        "markets": ["NSE", "BSE", "US", "CRYPTO"],
        "features": [
            "authentication",
            "multi_tenant_workspaces",
            "watchlists",
            "portfolios",
            "research",
            "investment_committee",
            "strategy_lab",
            "backtesting",
            "portfolio_intelligence",
            "trade_journal",
            "paper_trading",
        ],
        "live_order_execution": False,
        "data_mode": "demo_until_provider_configured",
    }
