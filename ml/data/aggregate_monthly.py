"""
Sprint 1 - Task 1.1 & 1.2: Monthly product aggregation + full time index.
Outputs: monthly_product_aggregation.csv, monthly_product_full.csv
"""
import pandas as pd
from pathlib import Path

# Paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = PROJECT_ROOT / "ecommerce_dataset_colab.csv"
DATA_DIR = Path(__file__).resolve().parent
OUT_AGG = DATA_DIR / "monthly_product_aggregation.csv"
OUT_FULL = DATA_DIR / "monthly_product_full.csv"


def main():
    # Load raw events
    df = pd.read_csv(RAW_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Task 1.1: only purchases
    purchases = df[df["event_type"] == "satın_alma"].copy()
    purchases["year_month"] = purchases["timestamp"].dt.to_period("M").astype(str)

    purchases["revenue"] = purchases["price"] * purchases["quantity"]
    agg = (
        purchases.groupby(["year_month", "product_id", "category"], as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
        )
    )

    agg.to_csv(OUT_AGG, index=False)
    print(f"Wrote {OUT_AGG} rows={len(agg)}")

    # Task 1.2: full monthly index per product, fill missing with 0
    all_months = sorted(agg["year_month"].unique())
    product_categories = agg.groupby("product_id")["category"].first()

    rows = []
    for product_id in agg["product_id"].unique():
        cat = product_categories[product_id]
        prod_agg = agg[agg["product_id"] == product_id].set_index("year_month")
        for ym in all_months:
            if ym not in prod_agg.index:
                qty = 0
                rev = 0.0
            else:
                qty = int(prod_agg.loc[ym, "total_quantity"])
                rev = float(prod_agg.loc[ym, "total_revenue"])
            rows.append({"year_month": ym, "product_id": product_id, "category": cat, "total_quantity": qty, "total_revenue": rev})

    full = pd.DataFrame(rows)
    full.to_csv(OUT_FULL, index=False)
    print(f"Wrote {OUT_FULL} rows={len(full)}")


if __name__ == "__main__":
    main()
