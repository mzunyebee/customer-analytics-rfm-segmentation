# Customer Analytics & RFM Segmentation

A customer analytics project using synthetic transaction data to group customers by **Recency, Frequency and Monetary value (RFM)** and support retention decisions.

## Business questions
- Who are the highest-value customers?
- Which customers have not purchased recently but historically transact frequently?
- How are customers distributed across segments?
- Which segments contribute the most revenue?

## Stack
SQL (SQLite-compatible), Python (pandas), Power BI (DAX).

## Run the Python analysis
```bash
python -m pip install pandas
python python/rfm_analysis.py
```
This creates `data/rfm_customer_segments.csv`.

## Run the SQL analysis
1. Create a SQLite database.
2. Run `sql/schema.sql`.
3. Import `data/customers.csv` and `data/transactions.csv` into their matching tables.
4. Run `sql/rfm_analysis.sql`.

## Power BI
Import the three CSV files from `data/`. Create relationships on `CustomerID`, then add measures from `power_bi/measures.dax`. Suggested visuals: segment revenue bar chart, customer count by segment, county slicer, and KPI cards.

## Methodology
Recency is days since the last purchase as at 31 December 2025. Frequency is transaction count. Monetary is total transaction value in KES. Quintile scores are combined into practical customer segments. Segment rules are illustrative and should be calibrated with business stakeholders.

## Data note
All customer and transaction records are synthetic, not real personal or commercial data.
