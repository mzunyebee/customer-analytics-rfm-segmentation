"""Customer RFM segmentation using pandas. Run from this folder or project root."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
customers = pd.read_csv(ROOT / "data" / "customers.csv")
tx = pd.read_csv(ROOT / "data" / "transactions.csv", parse_dates=["TransactionDate"])
as_of = pd.Timestamp("2025-12-31")

rfm = tx.groupby("CustomerID").agg(
    LastPurchase=("TransactionDate", "max"),
    Frequency=("TransactionID", "count"),
    MonetaryKES=("AmountKES", "sum")
).reset_index()
rfm["RecencyDays"] = (as_of - rfm["LastPurchase"]).dt.days
rfm = customers.merge(rfm, on="CustomerID", how="left")
rfm["Frequency"] = rfm["Frequency"].fillna(0)
rfm["MonetaryKES"] = rfm["MonetaryKES"].fillna(0)
rfm["RecencyDays"] = rfm["RecencyDays"].fillna((as_of - pd.Timestamp("2024-01-01")).days + 1)

# Quintile scoring. Reverse recency so a more recent purchase receives a higher score.
# Rank recency in reverse: the smallest number of days since purchase gets score 5.
rfm["RScore"] = pd.qcut(
    rfm["RecencyDays"].rank(method="first", ascending=False),
    5, labels=[1, 2, 3, 4, 5]
).astype(int)
for col, score_col in [("Frequency", "FScore"), ("MonetaryKES", "MScore")]:
    rfm[score_col] = pd.qcut(
        rfm[col].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
    ).astype(int)

def segment(row):
    r, f, m = row["RScore"], row["FScore"], row["MScore"]
    if r >= 4 and f >= 4 and m >= 4: return "Champions"
    if r >= 3 and f >= 3: return "Loyal Customers"
    if r >= 4 and f <= 2: return "New / Promising"
    if r <= 2 and f >= 3: return "At Risk"
    return "Needs Attention"

rfm["Segment"] = rfm.apply(segment, axis=1)
rfm.to_csv(ROOT / "data" / "rfm_customer_segments.csv", index=False)
print(rfm.groupby("Segment").agg(Customers=("CustomerID", "nunique"), RevenueKES=("MonetaryKES", "sum")).sort_values("RevenueKES", ascending=False))
