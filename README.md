# KukFin

KukFin is an AI-powered market research, portfolio intelligence, strategy backtesting, trade-journal, alerts, and paper-trading platform by Kuklabs.

> Status: authenticated SaaS foundation is runnable. No real-money order execution is enabled.

## Product boundaries

- Research and educational tooling, not personalized investment advice.
- All demo or delayed prices must be labelled.
- Live brokerage execution remains disabled until security, compliance, broker certification, and risk controls are complete.

## Implemented now

- Next.js public site, registration, login, and authenticated workspace dashboard.
- JWT access tokens with PBKDF2 password hashing.
- Tenant-isolated users, workspaces, memberships, watchlists, portfolios, and holdings.
- PostgreSQL persistence with Alembic migrations.
- FastAPI readiness, capability, authentication, watchlist, and portfolio endpoints.
- Docker images for web and API plus PostgreSQL and Redis services.
- CI web build, Python linting, and authenticated API integration test.

## Architecture

```text
apps/web                  Next.js web application
services/api              FastAPI gateway and SaaS API
services/quant-engine     Vibe-Trading/vectorbt adapters
services/research-engine  Deep research, earnings intelligence, trust gates
services/committee        Multi-agent investment committee
services/workers          Scheduled and asynchronous jobs
packages/contracts        Shared API contracts
infra                     Docker, deployment, and observability
```

See `docs/ROADMAP.md` and `docs/ARCHITECTURE.md`.

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

The API container applies Alembic migrations before starting.

- Web: http://localhost:3000
- Registration: http://localhost:3000/register
- Login: http://localhost:3000/login
- Workspace: http://localhost:3000/dashboard
- API: http://localhost:8000
- OpenAPI: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Readiness: http://localhost:8000/ready
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Current API surface

```text
POST   /v1/auth/register
POST   /v1/auth/login
GET    /v1/auth/me
GET    /v1/watchlist
POST   /v1/watchlist
DELETE /v1/watchlist/{item_id}
GET    /v1/portfolios
POST   /v1/portfolios
POST   /v1/portfolios/{portfolio_id}/holdings
GET    /v1/system/capabilities
```

## Upstream projects

KukFin integrates selected capabilities through adapters rather than copying repositories into one runtime:

- HKUDS/Vibe-Trading — quant research and backtesting
- virattt/ai-hedge-fund — investment committee workflow patterns
- Shubhamsaboo/awesome-llm-apps — research, earnings, and trust-gate patterns
- vectorbt — fast parameter exploration
- LEAN — optional future advanced execution engine

Each upstream dependency must retain its required license notices and attribution.
