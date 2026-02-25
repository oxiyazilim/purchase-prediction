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
