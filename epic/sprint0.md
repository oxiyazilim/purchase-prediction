purchase-prediction/
│
├── services/
│   ├── forecast/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── model_loader.py
│   │   │   └── schemas.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── decision/
│       ├── app/
│       │   ├── main.py
│       │   ├── logic.py
│       │   └── schemas.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── ml/
│   ├── data/
│   ├── features/
│   ├── training/
│   └── pipelines/
│
├── infra/
│   ├── terraform/
│   └── docker-compose.yml   # forecast, decision, mlflow, postgres, prometheus, grafana
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│
├── notebooks/
│
├── requirements.txt   # shared dev deps
├── .gitignore
├── README.md
└── AI_PLATFORM_STRATEGY.md

📦 Docker Stratejisi

Şu an:

- Her servis ayrı image
- docker-compose local orchestration
- Internal network

Port planı:

- forecast → 8001
- decision → 8002
- mlflow → 5000
- postgres → 5432 (MLflow backend)
- prometheus → 9090
- grafana → 3000

Hedef endpoint'ler (Strategy §4.5): forecast servisi → /forecast, /model-info, /metrics, /health; decision servisi → /decision, /health.

🧪 İlk Kod Adımı

Bugün yapmanı istediğim şey:

Repo oluştur

Bu klasör yapısını kur

Forecast servisine minimal FastAPI app koy:

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

Dockerfile yaz

docker-compose ile ayağa kaldır

Henüz ML yok.

Ama sistem ayağa kalkmalı.

🎯 Mental Model

Biz şu an model yapmıyoruz.

Biz:

AI sisteminin iskeletini kuruyoruz.