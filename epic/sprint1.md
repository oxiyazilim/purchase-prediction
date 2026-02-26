# SPRINT 1 — Product-Level Monthly Forecast (Foundation Phase)

## 🎯 Sprint Objective

Build a leakage-free, time-aware, product-level monthly dataset and train the first baseline + XGBoost forecasting model.

Target:
Predict next-month total_quantity per product (t → t+1).

---

# 1️⃣ Data Aggregation Layer

## Task 1.1 – Monthly Product Aggregation

Create dataset:

| year_month | product_id | category | total_quantity | total_revenue |

Rules:

* Use only event_type == "satın_alma"
* total_quantity = sum(quantity)
* total_revenue = sum(price * quantity)

Output: monthly_product_aggregation.csv

---

## Task 1.2 – Full Time Index

For each product:

* Create full monthly index
* Fill missing months with 0 quantity

Important:
Missing ≠ unknown.
Zero means no sales.

---

# 2️⃣ Feature Engineering Layer

All features must be computed with shift(1).
No leakage allowed.

## Lag Features

* lag_1
* lag_2
* lag_3

## Rolling Features

* rolling_3_mean
* rolling_3_std

## Trend

* momentum = lag_1 - lag_2

## Category Context

* category_total_monthly_sales
* product_share_in_category
* category_growth_rate

## Time Encoding

* month_sin
* month_cos

Drop rows with insufficient lag history.

Output: model_ready_dataset.csv

---

# 3️⃣ Target Definition

Target = next month quantity

For each product:

target = total_quantity.shift(-1)

Remove last month (no future label).

---

# 4️⃣ Train/Test Split

Time-based split only.

Train: All months except last 2
Test: Last 2 months

No random split.

---

# 5️⃣ Model Pipeline

Use sklearn Pipeline + ColumnTransformer.

Categorical:

* product_id → OneHotEncoder

Numeric:

* lag_1
* lag_2
* lag_3
* rolling_3_mean
* rolling_3_std
* momentum
* product_share_in_category
* category_growth_rate
* month_sin
* month_cos

Model:

* XGBRegressor

---

# 6️⃣ Evaluation

Metrics:

* MAE
* RMSE
* MAPE

Extract:

* Top 5 feature importances

---

# 7️⃣ MLflow Integration

Log:

* Parameters
* Metrics
* Model artifact

Register model as:
"product_monthly_forecast_v1"

---

# 📦 Sprint 1 Deliverables

You must report:

* Total dataset rows
* Unique products
* Train size
* Test size
* MAE
* MAPE
* Top 5 features

No deployment yet.
No decision engine yet.

This sprint is about clean forecasting foundation.

---

## YAPILANLAR (Sprint 1 özeti)

### Veri katmanı

| Dosya / klasör | Amaç |
|----------------|------|
| **`ml/data/aggregate_monthly.py`** | Task 1.1 + 1.2: Sadece `event_type == "satın_alma"` ile aylık ürün agregasyonu; ardından her ürün için tam aylık indeks, eksik aylar 0 ile doldurulur. |
| → Çıktı **`ml/data/monthly_product_aggregation.csv`** | year_month, product_id, category, total_quantity, total_revenue. |
| → Çıktı **`ml/data/monthly_product_full.csv`** | Tüm (year_month × product_id) kombinasyonları; satış yoksa total_quantity=0. |

### Özellik mühendisliği

| Dosya | Amaç |
|-------|------|
| **`ml/features/build_features.py`** | Tüm özellikler shift(1) ile (sızıntı yok). Lag 1–3, rolling_3 mean/std, momentum, kategori payı ve büyüme, month_sin/cos; target = bir sonraki ay quantity; yetersiz geçmiş olan satırlar atılır. |
| → Çıktı **`ml/data/model_ready_dataset.csv`** | Model girişi: product_id, category, lag/rolling/momentum/category/time özellikleri, target. |

### Eğitim pipeline

| Dosya | Amaç |
|-------|------|
| **`ml/training/train.py`** | Zaman tabanlı bölme: son 2 ay test, geri kalan train. sklearn Pipeline + ColumnTransformer (product_id → OneHotEncoder; sayısal özellikler passthrough) + XGBRegressor. |
| → **`mae`, `rmse`, `mape`** | Test seti üzerinde hesaplanır. |
| → **Top 5 feature importance** | XGBoost’tan çıkarılır. |
| → **MLflow** | Kuruluysa: parametreler, metrikler, model artifact; model adı: `product_monthly_forecast_v1`. Yerel `ml/mlruns` veya `MLFLOW_TRACKING_URI`. |
| **`ml/requirements.txt`** | pandas, numpy, scikit-learn, xgboost, mlflow. |

### Çalıştırma sırası

1. `python ml/data/aggregate_monthly.py` → aggregation + full index CSV’ler.
2. `python ml/features/build_features.py` → model_ready_dataset.csv.
3. `python ml/training/train.py` → eğitim + rapor (ve isteğe bağlı MLflow log).

### Örnek rapor (son çalıştırma)

- Total dataset rows: 560  
- Unique products: 70  
- Train size: 420, Test size: 140  
- MAE: ~15.13, RMSE: (scriptte yazdırılır), MAPE: ~11.46%  
- Top 5: product_id_203, month_cos, product_id_301, product_id_202, product_id_120 (önem sırasına göre).
