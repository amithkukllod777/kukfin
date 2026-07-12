from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: datetime


app = FastAPI(
    title="KukFin API",
    version="0.1.0",
    description="SaaS gateway for KukFin research and portfolio intelligence.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="kukfin-api",
        timestamp=datetime.now(UTC),
    )


@app.get("/v1/system/capabilities", tags=["system"])
def capabilities() -> dict[str, object]:
    return {
        "markets": ["NSE", "BSE", "US", "CRYPTO"],
        "features": [
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
