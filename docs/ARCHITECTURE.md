# KukFin Architecture

## Core principle

KukFin is a modular SaaS platform. External research and quant projects are integrated behind stable adapters; their internal models and workflows must not leak into the product UI or database schema.

## Services

### Web application

Next.js + TypeScript. Handles public pages, authentication flows, dashboards, research sessions, portfolios, strategy configuration, reports, and administration.

### API gateway

FastAPI. Owns authentication enforcement, tenant boundaries, request validation, audit events, rate limits, orchestration, and public API contracts.

### Quant engine

Python service providing strategy compilation, transaction-cost modelling, backtests, validation, factor analysis, and portfolio risk calculations. Vibe-Trading and vectorbt are accessed through adapters.

### Research engine

Plans research, gathers sources, records citations, detects conflicts, assigns confidence, and blocks claims that fail evidence thresholds. Earnings-call analysis is handled here.

### Investment committee

Runs independent fundamental, valuation, technical, sentiment, macro, and tail-risk agents. A portfolio-manager stage aggregates evidence and disagreement. Outputs are research opinions, not executable orders.

### Workers

Runs scheduled research, alerts, report generation, imports, and long backtests. Redis is the initial queue/cache dependency; the worker API remains replaceable.

## Data ownership

PostgreSQL is the system of record for tenants, users, memberships, portfolios, holdings, watchlists, research sessions, citations, strategies, backtests, paper accounts, alerts, reports, and audit events.

Market time-series and generated artifacts should move to dedicated object/time-series storage when volume requires it.

## Security boundaries

- Tenant ID is mandatory on tenant-owned rows.
- Provider and broker secrets never reach browser code.
- Real-money order execution is disabled.
- Paper trading is visibly labelled as simulated.
- Every generated recommendation stores model, prompt version, evidence, timestamps, and confidence.
- All privileged actions generate audit events.

## Initial API namespaces

- `/v1/auth`
- `/v1/markets`
- `/v1/research`
- `/v1/committee`
- `/v1/strategies`
- `/v1/backtests`
- `/v1/portfolios`
- `/v1/journal`
- `/v1/paper`
- `/v1/alerts`
- `/v1/reports`
- `/v1/admin`
