import os
from pathlib import Path

TEST_DB = Path("test_kukfin.db")
if TEST_DB.exists():
    TEST_DB.unlink()

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///./test_kukfin.db"
os.environ["JWT_SECRET"] = "test-secret-that-is-long-enough-for-ci"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def test_authenticated_portfolio_flow() -> None:
    with TestClient(app) as client:
        registration = client.post(
            "/v1/auth/register",
            json={
                "email": "founder@kuklabs.com",
                "full_name": "KukFin Founder",
                "password": "safe-test-password",
                "workspace_name": "Kuklabs",
            },
        )
        assert registration.status_code == 201
        token = registration.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        me = client.get("/v1/auth/me", headers=headers)
        assert me.status_code == 200
        assert me.json()["workspace_name"] == "Kuklabs"

        watchlist = client.post(
            "/v1/watchlist",
            headers=headers,
            json={"symbol": "RELIANCE", "exchange": "NSE", "note": "Core research"},
        )
        assert watchlist.status_code == 201

        portfolio = client.post(
            "/v1/portfolios",
            headers=headers,
            json={"name": "India Core", "base_currency": "INR"},
        )
        assert portfolio.status_code == 201
        portfolio_id = portfolio.json()["id"]

        holding = client.post(
            f"/v1/portfolios/{portfolio_id}/holdings",
            headers=headers,
            json={
                "symbol": "TCS",
                "exchange": "NSE",
                "quantity": 10,
                "average_price": 3850,
            },
        )
        assert holding.status_code == 201

        portfolios = client.get("/v1/portfolios", headers=headers)
        assert portfolios.status_code == 200
        assert portfolios.json()[0]["holdings"][0]["symbol"] == "TCS"
