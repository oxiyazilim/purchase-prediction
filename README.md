# Purchase Prediction – AI Demand & Decision Platform

Skeleton for the AI-driven demand forecasting and decision platform. See [AI_PLATFORM_STRATEGY.md](AI_PLATFORM_STRATEGY.md) for architecture and [epic/sprint0.md](epic/sprint0.md) for setup.

## Quick start (Docker)

From repo root:

```bash
cd infra
docker compose up --build
```

- **Forecast API:** http://localhost:8001 (e.g. GET /health)
- **Decision API:** http://localhost:8002 (e.g. GET /health)
- **MLflow:** http://localhost:5000
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin / admin)

## Project layout

- `services/forecast` – demand forecast FastAPI service
- `services/decision` – decision engine FastAPI service
- `ml/` – data, features, training, pipelines
- `infra/` – docker-compose, Terraform
- `monitoring/` – Prometheus, Grafana config
- `notebooks/` – exploration and experiments

No ML yet; this is the system skeleton.
