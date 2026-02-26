"""
Sprint 1 - Feature engineering: lag, rolling, trend, category context, time encoding.
All features use shift(1) for no leakage. Output: model_ready_dataset.csv
"""
import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FULL_PATH = DATA_DIR / "monthly_product_full.csv"
OUT_PATH = DATA_DIR / "model_ready_dataset.csv"


def main():
    df = pd.read_csv(FULL_PATH)
    df["year_month"] = pd.to_datetime(df["year_month"] + "-01")

    # Sort for shift operations
    df = df.sort_values(["product_id", "year_month"]).reset_index(drop=True)

    # Category totals per month (for category features)
    cat_monthly = df.groupby(["year_month", "category"])["total_quantity"].sum().reset_index()
    cat_monthly = cat_monthly.rename(columns={"total_quantity": "category_total_monthly_sales"})

    # Per-product time series: lags and rolling on past data only (shift(1))
    def build_product_features(g):
        g = g.sort_values("year_month")
        q = g["total_quantity"]
        # Lags (past months)
        g = g.assign(
            lag_1=q.shift(1),
            lag_2=q.shift(2),
            lag_3=q.shift(3),
        )
        # Rolling on shifted series so no future leakage
        g["rolling_3_mean"] = q.shift(1).rolling(3).mean()
        g["rolling_3_std"] = q.shift(1).rolling(3).std()
        g["momentum"] = g["lag_1"] - g["lag_2"]
        return g

    df = df.groupby("product_id", group_keys=True).apply(build_product_features)
    df = df.reset_index()  # product_id was in index after groupby

    # Category totals and growth rate (per category, then shift for no leakage)
    cat_monthly = cat_monthly.sort_values(["category", "year_month"])
    cat_monthly["cat_prev"] = cat_monthly.groupby("category")["category_total_monthly_sales"].shift(1)
    cat_monthly["category_growth_rate"] = np.where(
        cat_monthly["cat_prev"] > 0,
        (cat_monthly["category_total_monthly_sales"] - cat_monthly["cat_prev"]) / cat_monthly["cat_prev"],
        0,
    )
    cat_monthly = cat_monthly[["year_month", "category", "category_total_monthly_sales", "category_growth_rate"]]

    # Single merge: add category features (at current month; we'll shift next)
    df = df.merge(cat_monthly, on=["year_month", "category"], how="left")

    # Use past only: shift(1) category features per product
    df = df.sort_values(["product_id", "year_month"]).reset_index(drop=True)
    df["_cat_total_prev"] = df.groupby("product_id")["category_total_monthly_sales"].shift(1)
    df["category_growth_rate"] = df.groupby("product_id")["category_growth_rate"].shift(1)
    df["product_share_in_category"] = np.where(
        df["_cat_total_prev"] > 0,
        df.groupby("product_id")["total_quantity"].shift(1) / df["_cat_total_prev"],
        0,
    )
    df["category_total_monthly_sales"] = df["_cat_total_prev"]
    df = df.drop(columns=["_cat_total_prev"])

    # Time encoding: month of the row (period we're predicting for is next month; month of row = last known)
    month = df["year_month"].dt.month
    df["month_sin"] = np.sin(2 * np.pi * month / 12)
    df["month_cos"] = np.cos(2 * np.pi * month / 12)

    # Target: next month quantity
    df["target"] = df.groupby("product_id")["total_quantity"].shift(-1)

    # Drop rows with insufficient lag (need 3 past months) and last month (no target)
    df = df.dropna(subset=["lag_1", "lag_2", "lag_3", "rolling_3_mean", "rolling_3_std", "target"])

    # Drop helper columns we don't use as features
    df = df.drop(columns=["total_revenue", "category_total_monthly_sales"], errors="ignore")

    df.to_csv(OUT_PATH, index=False)
    print(f"Wrote {OUT_PATH} rows={len(df)}")


if __name__ == "__main__":
    main()
