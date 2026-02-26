"""
Sprint 1 - Training pipeline: sklearn Pipeline + ColumnTransformer, XGBoost, MLflow.
Time-based split: train = all except last 2 months, test = last 2 months.
"""
import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error
import xgboost as xgb
try:
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False

# Paths
ML_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ML_ROOT / "data"
DATASET_PATH = DATA_DIR / "model_ready_dataset.csv"

# Feature columns per spec
CATEGORICAL_FEATURES = ["product_id"]
NUMERIC_FEATURES = [
    "lag_1", "lag_2", "lag_3",
    "rolling_3_mean", "rolling_3_std",
    "momentum",
    "product_share_in_category", "category_growth_rate",
    "month_sin", "month_cos",
]
TARGET = "target"
TIME_COL = "year_month"

MODEL_NAME = "product_monthly_forecast_v1"


def mape(y_true, y_pred):
    """MAPE; avoid div by zero."""
    mask = y_true != 0
    if mask.sum() == 0:
        return np.nan
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def main():
    df = pd.read_csv(DATASET_PATH)
    df[TIME_COL] = pd.to_datetime(df[TIME_COL])
    df = df.sort_values(TIME_COL).reset_index(drop=True)

    # Time-based split: last 2 months = test
    unique_months = sorted(df[TIME_COL].unique())
    test_months = unique_months[-2:]
    train_df = df[~df[TIME_COL].isin(test_months)]
    test_df = df[df[TIME_COL].isin(test_months)]

    X_train = train_df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    y_train = train_df[TARGET]
    X_test = test_df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    y_test = test_df[TARGET]

    # Pipeline: ColumnTransformer (one-hot + passthrough numeric) then XGBoost
    preprocessor = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
            ("num", "passthrough", NUMERIC_FEATURES),
        ],
        remainder="drop",
    )
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
    )
    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", model),
    ])

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape_val = mape(y_test.values, y_pred)

    reg = pipe.named_steps["regressor"]
    pre = pipe.named_steps["preprocessor"]
    cat_names = pre.named_transformers_["cat"].get_feature_names_out(CATEGORICAL_FEATURES)
    feature_names = list(cat_names) + NUMERIC_FEATURES
    importances = reg.feature_importances_
    importance_list = sorted(zip(feature_names, importances), key=lambda x: -x[1])
    top5 = importance_list[:5]

    if MLFLOW_AVAILABLE:
        mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", str(ML_ROOT / "mlruns")))
        mlflow.set_experiment("sprint1_product_monthly_forecast")
        with mlflow.start_run():
            mlflow.log_params({
                "train_months": len(unique_months) - 2,
                "test_months": 2,
                "model_type": "XGBRegressor",
                "n_estimators": model.n_estimators,
                "max_depth": model.max_depth,
                "learning_rate": model.learning_rate,
            })
            mlflow.log_metrics({"mae": mae, "rmse": rmse, "mape": mape_val})
            for i, (name, imp) in enumerate(top5):
                mlflow.log_param(f"top5_feature_{i+1}", name)
                mlflow.log_metric(f"top5_importance_{i+1}", float(imp))
            mlflow.sklearn.log_model(pipe, "model", registered_model_name=MODEL_NAME)

    # Report deliverables
    n_products = df["product_id"].nunique()
    print("\n--- Sprint 1 Deliverables ---")
    print(f"Total dataset rows:     {len(df)}")
    print(f"Unique products:       {n_products}")
    print(f"Train size:            {len(train_df)}")
    print(f"Test size:             {len(test_df)}")
    print(f"MAE:                   {mae:.4f}")
    print(f"RMSE:                  {rmse:.4f}")
    print(f"MAPE:                  {mape_val:.2f}%")
    print("Top 5 feature importances:")
    for name, imp in top5:
        print(f"  {name}: {imp:.4f}")


if __name__ == "__main__":
    main()
