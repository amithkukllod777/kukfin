# KukFin

KukFin is an AI-powered market research, portfolio intelligence, strategy backtesting, trade-journal, alerts, and paper-trading platform by Kuklabs.

> Status: production foundation in progress. No real-money order execution is enabled.

## Product boundaries

- Research and educational tooling, not personalized investment advice.
- All demo or delayed prices must be labelled.
- Live brokerage execution remains disabled until security, compliance, broker certification, and risk controls are complete.

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

## Local foundation

```bash
cp .env.example .env
docker compose up --build
```

Initial services:

- Web: http://localhost:3000
- API: http://localhost:8000
- API health: http://localhost:8000/health
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Upstream projects

KukFin integrates selected capabilities through adapters rather than copying repositories into one runtime:

- HKUDS/Vibe-Trading — quant research and backtesting
- virattt/ai-hedge-fund — investment committee workflow patterns
- Shubhamsaboo/awesome-llm-apps — research, earnings, and trust-gate patterns
- vectorbt — fast parameter exploration
- LEAN — optional future advanced execution engine

Each upstream dependency must retain its required license notices and attribution.