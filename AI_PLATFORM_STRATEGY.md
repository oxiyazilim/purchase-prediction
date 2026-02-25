# AI-Driven Demand & Decision Platform

# 1. Executive Summary

This project simulates the design of an AI Platform inside an e-commerce company.
The objective is not only to forecast demand, but to convert predictive outputs into structured, risk-aware business decisions and deploy them in a production-ready architecture.

The system demonstrates:
- End-to-end ML lifecycle management
- Decision intelligence layer on top of forecasting
- Governance, retraining and monitoring strategy
- Containerized local development
- Infrastructure-as-Code based AWS deployment

---

# 2. Business & ML Problem

## 2.1 Business Problem
The company must decide:
- How to reallocate advertising budget next month
- Which product categories to prioritize
- How much to scale inventory investments
- What the financial risk is if the forecast is wrong

The goal is profit-aware, risk-adjusted decision making.

## 2.2 ML Problem
Given historical event-level e-commerce data, predict next-month category-level demand and quantify uncertainty.

Outputs:
- Demand delta per category
- Confidence score
- Volatility score
- Historical error reference

---

# 3. High-Level System Architecture

## 3.1 Logical Architecture Layers

1. Data Layer
2. Feature Engineering Layer
3. Forecasting Layer
4. Decision Engine Layer
5. Serving Layer
6. Monitoring & Governance Layer

Data flows forward. Monitoring feeds backward.

---

# 4. Detailed System Components

## 4.1 Data Layer

Responsibilities:
- Raw CSV ingestion
- Cleaning and normalization
- Time-based splitting
- Versioning with DVC

Local:
- CSV files
- DVC local storage

AWS (10x scale):
- S3 bucket (Parquet format)
- Versioned dataset snapshots

---

## 4.2 Feature Engineering Layer

Responsibilities:
- Rolling 30-day aggregates
- Category-level demand trends
- Segment-level uplift metrics
- Special day indicators
- Volatility metrics

Design principle:
Feature pipeline must be reproducible and independent of notebook logic.

---

## 4.3 Forecasting Layer

Models:
- Baseline (lag-based)
- XGBoost regression
- Prophet comparison

Experiment tracking:
- MLflow
- Parameter logging
- Metric comparison
- Model artifact storage

Model selection principle:
Trade-off between accuracy, interpretability and stability.

---

## 4.4 Decision Engine Layer

Purpose:
Transform forecast outputs into structured business actions.

Inputs:
- Forecast delta
- Confidence score
- Historical forecast error
- Volatility

Outputs:
- Recommended ad budget adjustment
- Inventory scaling recommendation
- Risk classification (Low / Medium / High)

Design:
- Rule-based threshold system
- Risk-adjusted action sizing
- Scenario simulation (low / expected / high demand)

---

## 4.5 Serving Layer

Technology:
- FastAPI
- Dockerized services

Endpoints:
- /forecast
- /decision
- /model-info
- /metrics
- /health

Architecture Option:
- Forecast service
- Decision service
(Separated containers for modularity)

---

## 4.6 Monitoring & Governance Layer

Monitoring:
- Prometheus metrics
- Grafana dashboards
- Forecast error tracking
- Drift signal detection

Governance:
- MLflow model registry
- Staging → Production promotion
- Manual approval gate
- Model version logging in every decision response

Rollback Strategy:
If new model performance degrades beyond threshold,
revert to last stable production version.

---

# 5. Deployment Strategy

# Phase 1 – Local Development

Environment:
- Docker Compose

Containers:
- FastAPI Forecast Service
- FastAPI Decision Service
- MLflow
- Postgres (MLflow backend)
- Prometheus
- Grafana

Goals:
- Production-like modular structure
- Container isolation
- Observability from day one

---

# Phase 2 – AWS Deployment (IaC with Terraform)

Core AWS Components:

- S3 → Data & model artifacts
- ECR → Docker images
- ECS or EKS → Container orchestration
- RDS → MLflow backend
- CloudWatch → Logs
- IAM → Fine-grained access control

Terraform Responsibilities:
- S3 bucket creation
- ECR repository
- ECS/EKS cluster
- Security groups
- IAM roles & policies

Deployment Flow:
1. Build Docker image
2. Push to ECR
3. Terraform apply
4. Deploy service
5. Health check validation

---

# 6. 10x Scale Adaptation Strategy

If traffic and data increase 10x:

Data:
- Move to Parquet
- Batch jobs in distributed compute (Spark/EMR)

Model Training:
- Separate training environment
- Scheduled retraining windows

Serving:
- Horizontal autoscaling
- Load balancer
- Resource-based scaling rules

Monitoring:
- Centralized logging (OpenSearch)
- Drift detection automation

Cost Control:
- Spot instances for training
- Autoscaling policies
- Storage lifecycle policies

---

# 7. Platform Mindset Summary

This project does not aim to maximize model accuracy alone.

It demonstrates:
- Structured ML lifecycle
- Risk-aware decision framework
- Cloud-native deployment thinking
- Governance & retraining discipline

The objective is not to build a model.
The objective is to demonstrate AI organizational capability.

---

# 8. System Architecture Diagram (Logical View)

Below is the logical flow of the system:

```
                +-------------------+
                |   Raw Sales Data  |
                +---------+---------+
                          |
                          v
                +-------------------+
                |  Data Processing  |
                |  (Clean + Split)  |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Feature Pipeline  |
                | (Rolling Metrics) |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Forecasting Layer |
                | (Baseline/XGB)    |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Decision Engine   |
                | Risk Adjustment   |
                +---------+---------+
                          |
                          v
                +-------------------+
                |  FastAPI Serving  |
                +---------+---------+
                          |
          +---------------+----------------+
          |                                |
          v                                v
   +-------------+                 +---------------+
   | Prometheus  |                 |  MLflow       |
   | Monitoring  |                 |  Registry     |
   +-------------+                 +---------------+
```

Monitoring feeds back into:
- Retraining trigger
- Governance checks
- Risk evaluation

---

# 9. Deployment Architecture (Infrastructure View)

## Phase 1 – Local (Docker Compose)

```
[Docker Host]
   ├── forecast-service
   ├── decision-service
   ├── mlflow
   ├── postgres
   ├── prometheus
   └── grafana
```

All services communicate over an internal Docker network.

---

## Phase 2 – AWS Architecture

```
                +----------------------+
                |        S3            |
                | (Data + Artifacts)   |
                +----------+-----------+
                           |
                           v
+----------------+   +-------------------+   +----------------+
|   ECR          |-->|   ECS / EKS       |-->|  Load Balancer |
| (Docker Images)|   |  Forecast +       |   |                |
+----------------+   |  Decision Pods    |   +----------------+
                     +---------+---------+
                               |
                               v
                        +--------------+
                        |   RDS        |
                        | (MLflow DB)  |
                        +--------------+
```

Logging:
- CloudWatch

Metrics:
- Prometheus (self-hosted or managed alternative)

---

# 10. CI/CD Architecture

We separate two pipelines:

## 10.1 Application Pipeline (Code Changes)

Trigger: Push to main branch

Steps:
1. Run unit tests
2. Run lint checks
3. Build Docker images
4. Push images to ECR
5. Deploy updated services to ECS/EKS
6. Health check validation

---

## 10.2 Model Pipeline (Model Changes)

Trigger:
- New training run
- Performance threshold breach

Steps:
1. Execute training pipeline
2. Log experiment in MLflow
3. Register model in staging
4. Manual approval gate
5. Promote to production
6. Update serving container with new model artifact

---

# 11. Pipeline Separation Principle

Application code lifecycle and model lifecycle are separated.

This ensures:
- Code updates do not automatically promote new models
- Model updates do not require full application redeploy
- Governance and auditability are preserved

This separation reflects enterprise AI platform sta