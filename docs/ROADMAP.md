# KukFin Production Roadmap

## Phase 0 — Foundation

- Monorepo structure
- Next.js web shell
- FastAPI service
- PostgreSQL and Redis
- Docker Compose
- Environment validation
- CI for web and API
- Architecture decision records

Exit: clean local boot, health checks, lint and tests pass.

## Phase 1 — Identity and tenancy

- Email/OAuth authentication
- User profiles
- Organizations and memberships
- Roles: user, analyst, admin
- Row-level tenant enforcement
- Audit log
- Session and API rate limits

Exit: isolated tenant accounts with tested authorization.

## Phase 2 — Market-data layer

- Instrument master for NSE, BSE, US equities, and crypto
- Provider adapter contracts
- Quotes and historical bars
- Fundamentals and corporate actions
- Data freshness and provenance
- India transaction-cost configuration

Exit: reliable delayed-data experience with provider fallbacks.

## Phase 3 — Research intelligence

- Conversational research
- Source retrieval and citation storage
- Claim-to-source mapping
- Conflict detection
- Confidence and trust gates
- Saved sessions and reports
- Earnings intelligence

Exit: evidence-backed reports with reproducible audit records.

## Phase 4 — Investment committee

- Fundamental, valuation, technical, sentiment, macro, and tail-risk agents
- Independent evidence collection
- Disagreement view
- Portfolio-manager aggregation
- Prompt and model versioning
- Cost and latency controls

Exit: structured committee reports without trade execution.

## Phase 5 — Strategy lab and backtesting

- Natural-language strategy specification
- Strategy schema and validation
- Vibe-Trading adapter
- vectorbt adapter
- Slippage, fees, STT, GST, stamp duty, exchange and SEBI charges
- Benchmarking, walk-forward tests, Monte Carlo and bias warnings

Exit: reproducible backtests with artifacts and validation warnings.

## Phase 6 — Portfolio and journal

- Portfolios and holdings
- Allocation and concentration analysis
- Correlation and scenario analysis
- Manual/CSV trade journal
- Thesis, tags, errors and behavioural insights

Exit: useful portfolio intelligence without broker write access.

## Phase 7 — Paper trading and alerts

- Simulated cash, positions and orders
- Price, technical, earnings and risk alerts
- Scheduled research
- Email and push adapters

Exit: fully labelled simulation and reliable alert delivery.

## Phase 8 — Commercial readiness

- Plans, usage metering and billing
- Admin operations
- Data retention and deletion
- Security review
- Observability, backups and disaster recovery
- Legal/compliance review
- Deployment at fin.kuklabs.com

Exit: production launch candidate.

## Deferred

Real-money broker execution, personalized investment advice, copy trading, leverage, derivatives execution, and managed-account features remain out of scope until separate regulatory and security approval.