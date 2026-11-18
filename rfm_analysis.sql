-- RFM analysis as at 2025-12-31
WITH customer_metrics AS (
  SELECT
    c.CustomerID,
    c.County,
    c.CustomerType,
    CAST(julianday('2025-12-31') - julianday(MAX(t.TransactionDate)) AS INTEGER) AS RecencyDays,
    COUNT(t.TransactionID) AS Frequency,
    ROUND(SUM(t.AmountKES), 2) AS MonetaryKES
  FROM customers c
  LEFT JOIN transactions t ON c.CustomerID = t.CustomerID
  GROUP BY c.CustomerID, c.County, c.CustomerType
),
scored AS (
  SELECT *,
    NTILE(5) OVER (ORDER BY RecencyDays DESC) AS R_Score,
    NTILE(5) OVER (ORDER BY Frequency ASC) AS F_Score,
    NTILE(5) OVER (ORDER BY MonetaryKES ASC) AS M_Score
  FROM customer_metrics
)
SELECT *,
  CASE
    WHEN R_Score >= 4 AND F_Score >= 4 AND M_Score >= 4 THEN 'Champions'
    WHEN R_Score >= 3 AND F_Score >= 3 THEN 'Loyal Customers'
    WHEN R_Score >= 4 AND F_Score <= 2 THEN 'New / Promising'
    WHEN R_Score <= 2 AND F_Score >= 3 THEN 'At Risk'
    ELSE 'Needs Attention'
  END AS Segment
FROM scored;
