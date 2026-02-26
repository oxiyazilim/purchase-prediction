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

---

## YAPILANLAR (Sprint 0 özeti)

### Klasörler ve amaçları

| Klasör / dosya | Amaç |
|----------------|------|
| **`services/`** | Uygulama servislerini (forecast, decision) barındırmak. |
| **`services/forecast/`** | Tahmin servisi: ileride ML modeli ile forecast üretecek. |
| **`services/forecast/app/`** | Forecast servisinin FastAPI uygulama kodu. |
| **`services/decision/`** | Karar servisi: ileride forecast çıktısına göre karar verecek. |
| **`services/decision/app/`** | Decision servisinin FastAPI uygulama kodu. |
| **`ml/`** | ML veri, feature, training ve pipeline’lar için iskelet (henüz boş). |
| **`infra/`** | Altyapı tanımları: docker-compose, MLflow Dockerfile. |
| **`monitoring/`** | Prometheus config; ileride Grafana dashboard’ları. |
| **`notebooks/`** | Analiz / deney not defterleri için (henüz boş). |

### Forecast servisi

| Dosya | Amaç |
|-------|------|
| **`services/forecast/app/main.py`** | FastAPI uygulaması; servisin giriş noktası. |
| → **`health()`** | Sağlık kontrolü: `GET /health` → `{"status": "ok"}`. Servisin ayakta olduğunu doğrulamak ve load balancer / orchestration için. |
| **`services/forecast/app/model_loader.py`** | Placeholder: ML eklendiğinde model yükleme burada olacak. |
| **`services/forecast/app/schemas.py`** | Placeholder: request/response şemaları ML eklendiğinde tanımlanacak. |
| **`services/forecast/Dockerfile`** | Forecast servisini Python 3.11-slim tabanlı image’e paketler; port 8001, uvicorn ile çalıştırır. |
| **`services/forecast/requirements.txt`** | Servis bağımlılıkları: FastAPI, uvicorn. |

### Decision servisi

| Dosya | Amaç |
|-------|------|
| **`services/decision/app/main.py`** | FastAPI uygulaması; servisin giriş noktası. |
| → **`health()`** | Sağlık kontrolü: `GET /health` → `{"status": "ok"}`. |
| **`services/decision/app/logic.py`** | Placeholder: karar mantığı ileride burada. |
| **`services/decision/app/schemas.py`** | Placeholder: request/response şemaları ileride. |
| **`services/decision/Dockerfile`** | Decision servisini port 8002 ile image’e paketler; uvicorn ile çalıştırır. |
| **`services/decision/requirements.txt`** | FastAPI, uvicorn. |

### Altyapı ve izleme

| Dosya | Amaç |
|-------|------|
| **`infra/docker-compose.yml`** | Tüm stack’i ayağa kaldırır: forecast (8001), decision (8002), postgres (5432), mlflow (5000), prometheus (9090), grafana (3000); `app` network’ü. |
| **`infra/mlflow/Dockerfile`** | MLflow server image’i; Postgres backend için psycopg2-binary ekler. |
| **`monitoring/prometheus.yml`** | Forecast ve decision servislerini hedefleyen scrape config’i (health vb. metrikler için hazırlık). |

### Kök seviye

| Dosya | Amaç |
|-------|------|
| **`requirements.txt`** | Ortak geliştirme bağımlılıkları (yerel çalıştırma, test, lint). |
| **`.gitignore`** | Git’e girmemesi gereken dosya/klasörler. |
| **`README.md`** | Proje tanımı ve kullanım. |
| **`AI_PLATFORM_STRATEGY.md`** | Platform strateji dokümanı. |

**Özet:** Repo ve hedeflenen klasör yapısı kuruldu; forecast ve decision servisleri minimal FastAPI ile sadece `/health` dönüyor; her iki servis için Dockerfile yazıldı; docker-compose ile forecast, decision, postgres, mlflow, prometheus, grafana ayağa kalkıyor. ML kodu yok, model_loader / schemas / logic dosyaları placeholder.
